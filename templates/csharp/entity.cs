using System;

namespace {{namespace}}.{{domain}}.Entities
{
    /// <summary>
    /// {{name}} Entity
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public class {{name}}
    {
        /// <summary>
        /// Gets the unique identifier for this {{name}}.
        /// </summary>
        public {{name}}Id Id { get; private set; }
        
        // TODO: Add domain-specific properties
        // Example properties following DDD patterns:
        
        // public UserName Name { get; private set; }
        // public Email Email { get; private set; }
        // public DateTime CreatedAt { get; private set; }
        // public DateTime? UpdatedAt { get; private set; }
        
        /// <summary>
        /// Initializes a new instance of the {{name}} class.
        /// </summary>
        /// <param name="id">The unique identifier.</param>
        protected {{name}}({{name}}Id id)
        {
            Id = id ?? throw new ArgumentNullException(nameof(id));
            // CreatedAt = DateTime.UtcNow;
        }
        
        /// <summary>
        /// Creates a new {{name}} instance.
        /// TODO: Replace with actual factory method parameters.
        /// </summary>
        /// <param name="id">The unique identifier.</param>
        /// <returns>A new {{name}} instance.</returns>
        public static {{name}} Create({{name}}Id id /* TODO: Add other parameters */)
        {
            // TODO: Add validation logic
            if (id == null)
                throw new ArgumentNullException(nameof(id));
            
            return new {{name}}(id);
        }
        
        // TODO: Add domain methods
        // Example domain methods:
        
        // public void UpdateName(UserName newName)
        // {
        //     if (newName == null)
        //         throw new ArgumentNullException(nameof(newName));
        //     
        //     Name = newName;
        //     UpdatedAt = DateTime.UtcNow;
        // }
        
        // public void ChangeEmail(Email newEmail)
        // {
        //     if (newEmail == null)
        //         throw new ArgumentNullException(nameof(newEmail));
        //     
        //     // Business logic for email change
        //     Email = newEmail;
        //     UpdatedAt = DateTime.UtcNow;
        // }
        
        /// <summary>
        /// Determines whether the specified object is equal to the current object.
        /// </summary>
        /// <param name="obj">The object to compare with the current object.</param>
        /// <returns>true if the specified object is equal to the current object; otherwise, false.</returns>
        public override bool Equals(object? obj)
        {
            if (obj is not {{name}} other)
                return false;
                
            return Id.Equals(other.Id);
        }
        
        /// <summary>
        /// Returns the hash code for this instance.
        /// </summary>
        /// <returns>A hash code for the current object.</returns>
        public override int GetHashCode()
        {
            return Id.GetHashCode();
        }
    }
}