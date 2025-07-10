using System;
using System.ComponentModel.DataAnnotations;

namespace {{namespace}}.{{domain}}.Usecases.{{name}}
{
    /// <summary>
    /// Request for {{name}} UseCase
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public class {{name}}Request
    {
        /// <summary>
        /// Gets or sets the example property.
        /// TODO: Replace with actual properties needed for this use case.
        /// </summary>
        [Required(ErrorMessage = "Example property is required.")]
        public string ExampleProperty { get; set; } = string.Empty;
        
        // TODO: Add additional properties as needed
        // Example properties:
        
        // [Required]
        // public string RequiredProperty { get; set; } = string.Empty;
        
        // [StringLength(100, MinimumLength = 3)]
        // public string Name { get; set; } = string.Empty;
        
        // [EmailAddress]
        // public string Email { get; set; } = string.Empty;
        
        // [Range(1, int.MaxValue)]
        // public int Id { get; set; }
        
        // public DateTime? OptionalDate { get; set; }
        
        /// <summary>
        /// Validates the request object.
        /// </summary>
        /// <returns>True if valid, false otherwise.</returns>
        public bool IsValid()
        {
            // TODO: Add custom validation logic
            return !string.IsNullOrWhiteSpace(ExampleProperty);
        }
    }
}