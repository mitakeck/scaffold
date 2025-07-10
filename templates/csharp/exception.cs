using System;

namespace {{namespace}}.{{domain}}.Exceptions
{
    /// <summary>
    /// Exception class for error code {{code}}
    /// {{name}} Exception
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public class {{code}}_{{name}}Exception : DomainException
    {
        /// <summary>
        /// Initializes a new instance of the {{code}}_{{name}}Exception class.
        /// </summary>
        public {{code}}_{{name}}Exception()
            : base("{{code}}", "{{message}}", "{{resolution}}")
        {
        }
        
        /// <summary>
        /// Initializes a new instance of the {{code}}_{{name}}Exception class with additional context.
        /// </summary>
        /// <param name="additionalInfo">Additional information to include in the error message.</param>
        public {{code}}_{{name}}Exception(string additionalInfo)
            : base("{{code}}", $"{{message}} ({{additionalInfo}})", "{{resolution}}")
        {
        }
        
        /// <summary>
        /// Initializes a new instance of the {{code}}_{{name}}Exception class with an inner exception.
        /// </summary>
        /// <param name="innerException">The exception that is the cause of the current exception.</param>
        public {{code}}_{{name}}Exception(Exception innerException)
            : base("{{code}}", "{{message}}", "{{resolution}}", innerException)
        {
        }
        
        /// <summary>
        /// Initializes a new instance of the {{code}}_{{name}}Exception class with additional context and an inner exception.
        /// </summary>
        /// <param name="additionalInfo">Additional information to include in the error message.</param>
        /// <param name="innerException">The exception that is the cause of the current exception.</param>
        public {{code}}_{{name}}Exception(string additionalInfo, Exception innerException)
            : base("{{code}}", $"{{message}} ({{additionalInfo}})", "{{resolution}}", innerException)
        {
        }
    }
    
    // TODO: Add base DomainException class if not already exists
    // Example base class:
    /*
    public abstract class DomainException : Exception
    {
        public string ErrorCode { get; }
        public string UserMessage { get; }
        public string Resolution { get; }
        
        protected DomainException(string errorCode, string userMessage, string resolution)
            : base($"{errorCode}: {userMessage}")
        {
            ErrorCode = errorCode;
            UserMessage = userMessage;
            Resolution = resolution;
        }
        
        protected DomainException(string errorCode, string userMessage, string resolution, Exception innerException)
            : base($"{errorCode}: {userMessage}", innerException)
        {
            ErrorCode = errorCode;
            UserMessage = userMessage;
            Resolution = resolution;
        }
    }
    */
}