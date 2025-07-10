using System;

namespace {{namespace}}.{{domain}}.Usecases.{{name}}
{
    /// <summary>
    /// Response for {{name}} UseCase
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public class {{name}}Response
    {
        /// <summary>
        /// Gets or sets a value indicating whether the operation was successful.
        /// </summary>
        public bool Success { get; set; }
        
        /// <summary>
        /// Gets or sets the response message.
        /// </summary>
        public string Message { get; set; } = string.Empty;
        
        /// <summary>
        /// Gets or sets the error code if operation failed.
        /// </summary>
        public string? ErrorCode { get; set; }
        
        // TODO: Add result properties specific to this use case
        // Example properties:
        
        // public string Id { get; set; } = string.Empty;
        // public DateTime CreatedAt { get; set; }
        // public string Name { get; set; } = string.Empty;
        // public List<string> ValidationErrors { get; set; } = new();
        
        /// <summary>
        /// Creates a successful response.
        /// </summary>
        /// <param name="message">Success message.</param>
        /// <returns>A successful response.</returns>
        public static {{name}}Response CreateSuccess(string message = "Operation completed successfully.")
        {
            return new {{name}}Response
            {
                Success = true,
                Message = message
            };
        }
        
        /// <summary>
        /// Creates a failure response.
        /// </summary>
        /// <param name="message">Error message.</param>
        /// <param name="errorCode">Error code.</param>
        /// <returns>A failure response.</returns>
        public static {{name}}Response CreateFailure(string message, string? errorCode = null)
        {
            return new {{name}}Response
            {
                Success = false,
                Message = message,
                ErrorCode = errorCode
            };
        }
    }
}