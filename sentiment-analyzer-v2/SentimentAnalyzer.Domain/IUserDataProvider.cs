using System.Threading.Tasks;
using SentimentAnalyzer.Domain.DTOs;

namespace SentimentAnalyzer.Domain
{
    public interface IUserDataProvider
    {
        Task InitAsync();
        Task<UserData> GetUserDataAsync(int userId);
    }
}
