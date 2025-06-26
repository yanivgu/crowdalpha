using System.Collections.Generic;

namespace SentimentAnalyzer.Infrastructure;

public interface ICsvAdapter<T>
{
    /// <summary>
    /// Returns the headers for the CSV file, in order.
    /// </summary>
    IReadOnlyList<string> Headers { get; }

    /// <summary>
    /// Parses a CSV line (as a list of fields) into an object of type T.
    /// </summary>
    T FromLine(IReadOnlyList<string> fields);

    /// <summary>
    /// Serializes an object of type T into one or more CSV lines (as strings).
    /// </summary>
    IReadOnlyList<string> ToLines(T obj);
}
