using System;

namespace {{namespace}}.{{domain}}.ValueObjects
{
    /// <summary>
    /// {{name}} Value Object
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public record {{name}}({{type}} Value)
    {
        /// <summary>
        /// Initializes a new instance of the {{name}} record.
        /// </summary>
        /// <param name="value">The underlying value.</param>
        /// <exception cref="ArgumentException">Thrown when the value is invalid.</exception>
        public {{name}}({{type}} value) : this(value)
        {
            // TODO: Add validation logic specific to this value object
            ValidateValue(value);
            Value = value;
        }
        
        /// <summary>
        /// Validates the provided value.
        /// </summary>
        /// <param name="value">The value to validate.</param>
        /// <exception cref="ArgumentException">Thrown when the value is invalid.</exception>
        private static void ValidateValue({{type}} value)
        {
            // TODO: Implement validation logic
            // Example validations:
            
            // For string values:
            // if (string.IsNullOrWhiteSpace(value))
            //     throw new ArgumentException("{{name}} cannot be null or empty.", nameof(value));
            
            // if (value.Length > 100)
            //     throw new ArgumentException("{{name}} cannot exceed 100 characters.", nameof(value));
            
            // For numeric values:
            // if (value <= 0)
            //     throw new ArgumentException("{{name}} must be greater than zero.", nameof(value));
            
            // For email format:
            // if (!IsValidEmailFormat(value))
            //     throw new ArgumentException("Invalid email format.", nameof(value));
        }
        
        // TODO: Add utility methods specific to this value object
        // Example methods:
        
        // /// <summary>
        // /// Checks if the email format is valid.
        // /// </summary>
        // /// <param name="email">The email to validate.</param>
        // /// <returns>True if valid, false otherwise.</returns>
        // private static bool IsValidEmailFormat(string email)
        // {
        //     return System.Net.Mail.MailAddress.TryCreate(email, out _);
        // }
        
        // /// <summary>
        // /// Returns the domain part of the email.
        // /// </summary>
        // /// <returns>The domain part.</returns>
        // public string GetDomain()
        // {
        //     return Value.Split('@')[1];
        // }
        
        /// <summary>
        /// Implicit conversion from {{type}} to {{name}}.
        /// </summary>
        /// <param name="value">The value to convert.</param>
        /// <returns>A new {{name}} instance.</returns>
        public static implicit operator {{name}}({{type}} value)
        {
            return new {{name}}(value);
        }
        
        /// <summary>
        /// Implicit conversion from {{name}} to {{type}}.
        /// </summary>
        /// <param name="{{name.ToLower()}}">The {{name}} to convert.</param>
        /// <returns>The underlying value.</returns>
        public static implicit operator {{type}}({{name}} {{name.ToLower()}})
        {
            return {{name.ToLower()}}.Value;
        }
        
        /// <summary>
        /// Returns a string representation of this value object.
        /// </summary>
        /// <returns>The string representation.</returns>
        public override string ToString()
        {
            return Value?.ToString() ?? string.Empty;
        }
    }
}