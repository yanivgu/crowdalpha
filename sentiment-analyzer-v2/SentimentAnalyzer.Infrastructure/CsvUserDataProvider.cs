using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using SentimentAnalyzer.Domain;
using SentimentAnalyzer.Domain.DTOs;

namespace SentimentAnalyzer.Infrastructure
{
    public class CsvUserDataProvider : IUserDataProvider
    {
        private readonly string _userDataCsvPath;
        private readonly string _userGainsCsvPath;
        private readonly CsvTextFileReader _fileReader;
        private Dictionary<int, UserData> _userDataDict;
        private bool _loaded;
        private static readonly SemaphoreSlim _semaphore = new SemaphoreSlim(1, 1);
        private readonly ILogger _logger;

        public CsvUserDataProvider(CsvTextFileReader fileReader, string userDataCsvPath, string userGainsCsvPath, ILogger logger)
        {
            _fileReader = fileReader;
            _userDataCsvPath = userDataCsvPath;
            _userGainsCsvPath = userGainsCsvPath;
            _userDataDict = new Dictionary<int, UserData>();
            _loaded = false;
            _logger = logger;
        }

        public async Task InitAsync()
        {
            await EnsureLoadedAsync();
        }

        private async Task EnsureLoadedAsync()
        {
            if (_loaded) return;
            await _semaphore.WaitAsync();
            try
            {
                if (_loaded) return;
                // Read user data first
                await foreach (var user in _fileReader.ReadLinesAsync(_userDataCsvPath, UserDataFileAdapter.Instance))
                {
                    if (user != null)
                    {
                        if (!_userDataDict.ContainsKey(user.UserId))
                            _userDataDict[user.UserId] = user;
                        else
                            _logger.Warn($"Duplicate user with ID {user.UserId} found in CSV. Skipping.");
                    }
                }
                _logger.Info($"Loaded {_userDataDict.Count} users from CSV file: {_userDataCsvPath}");
                // Read gains and update
                await foreach (var gain in _fileReader.ReadLinesAsync(_userGainsCsvPath, UserGainFileAdapter.Instance))
                {
                    if (gain != null && _userDataDict.TryGetValue(gain.UserId, out var userData))
                        userData.TwoYearGain = gain.TwoYearGain;
                }
                _logger.Info($"Updated gains for {_userDataDict.Count} users from CSV file: {_userGainsCsvPath}");
                _loaded = true;
            }
            finally
            {
                _semaphore.Release();
            }
        }

        public async Task<UserData> GetUserDataAsync(int userId)
        {
            await EnsureLoadedAsync();
            _userDataDict.TryGetValue(userId, out var userData);
            return userData;
        }

        private class UserDataFileAdapter : ICsvAdapter<UserData>
        {
            public static readonly UserDataFileAdapter Instance = new UserDataFileAdapter();
            private static readonly IReadOnlyList<string> _headers = new List<string> { "OwnerID", "PlayerLevel", "MonthsActive" };
            public IReadOnlyList<string> Headers => _headers;

            public UserData FromLine(IReadOnlyList<string> fields)
            {
                if (fields.Count != 3) throw new ArgumentException("Invalid fields for user data");
                return new UserData
                {
                    UserId = int.TryParse(fields[0], out var id) ? id : 0,
                    Level = fields[1],
                    MonthsActive = int.TryParse(fields[2], out var months) ? months : 0,
                    TwoYearGain = 0m
                };
            }

            public IReadOnlyList<string> ToLines(UserData obj)
            {
                throw new NotImplementedException();
            }
        }

        private class UserGainFileAdapter : ICsvAdapter<UserData>
        {
            public static readonly UserGainFileAdapter Instance = new UserGainFileAdapter();
            private static readonly IReadOnlyList<string> _headers = new List<string> { "id", "gain" };
            public IReadOnlyList<string> Headers => _headers;

            public UserData FromLine(IReadOnlyList<string> fields)
            {
                if (fields.Count != 2) throw new ArgumentException("Invalid fields for user gain");
                return new UserData
                {
                    UserId = int.TryParse(fields[0], out var id) ? id : 0,
                    TwoYearGain = decimal.TryParse(fields[1], NumberStyles.Any, CultureInfo.InvariantCulture, out var gain) ? gain : 0m
                };
            }

            public IReadOnlyList<string> ToLines(UserData obj)
            {
                throw new NotImplementedException();
            }
        }
    }
}
