using System;
using System.Threading.Tasks;

namespace {{namespace}}.{{domain}}.Usecases.{{name}}
{
    /// <summary>
    /// {{name}} UseCase
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public class {{name}}UseCase
    {
        // TODO: Add required dependencies (repositories, services, etc.)
        // private readonly I{{domain}}Repository _repository;
        
        /// <summary>
        /// Initializes a new instance of the {{name}}UseCase class.
        /// </summary>
        public {{name}}UseCase(/* TODO: Add dependencies */)
        {
            // TODO: Initialize dependencies
            // _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        }
        
        /// <summary>
        /// Executes the {{name}} use case.
        /// </summary>
        /// <param name="request">The request containing input parameters.</param>
        /// <returns>The response containing the result.</returns>
        public async Task<{{name}}Response> ExecuteAsync({{name}}Request request)
        {
            // TODO: Validate input
            if (request == null)
                throw new ArgumentNullException(nameof(request));
            
            try
            {
                // TODO: Implement business logic
                
                // Example implementation:
                // 1. Validate business rules
                // 2. Execute domain operations
                // 3. Persist changes
                // 4. Return response
                
                return new {{name}}Response
                {
                    // TODO: Set response properties
                    Success = true,
                    Message = "Operation completed successfully."
                };
            }
            catch (DomainException)
            {
                // Re-throw domain exceptions as-is
                throw;
            }
            catch (Exception ex)
            {
                // Wrap unexpected exceptions
                // TODO: Log the exception
                throw new SystemException("An unexpected error occurred during {{name}} execution.", ex);
            }
        }
    }
}