using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{namespace}}.{{domain}}.Repositories
{
    /// <summary>
    /// Repository interface for {{entity}} entities
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public interface I{{entity}}Repository
    {
        /// <summary>
        /// Gets a {{entity}} by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier.</param>
        /// <returns>The {{entity}} if found; otherwise, null.</returns>
        Task<{{entity}}?> GetByIdAsync({{entity}}Id id);
        
        /// <summary>
        /// Gets all {{entity}} entities.
        /// </summary>
        /// <returns>A collection of all {{entity}} entities.</returns>
        Task<IEnumerable<{{entity}}>> GetAllAsync();
        
        /// <summary>
        /// Saves a {{entity}} entity (insert or update).
        /// </summary>
        /// <param name="{{entity.ToLower()}}">The {{entity}} to save.</param>
        /// <returns>The saved {{entity}}.</returns>
        Task<{{entity}}> SaveAsync({{entity}} {{entity.ToLower()}});
        
        /// <summary>
        /// Deletes a {{entity}} by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier.</param>
        /// <returns>A task representing the asynchronous operation.</returns>
        Task DeleteAsync({{entity}}Id id);
        
        /// <summary>
        /// Checks if a {{entity}} exists with the specified identifier.
        /// </summary>
        /// <param name="id">The unique identifier.</param>
        /// <returns>True if the {{entity}} exists; otherwise, false.</returns>
        Task<bool> ExistsAsync({{entity}}Id id);
        
        // TODO: Add domain-specific query methods
        // Example methods:
        
        // /// <summary>
        // /// Gets {{entity}} entities by email.
        // /// </summary>
        // /// <param name="email">The email to search for.</param>
        // /// <returns>The {{entity}} if found; otherwise, null.</returns>
        // Task<{{entity}}?> GetByEmailAsync(Email email);
        
        // /// <summary>
        // /// Gets {{entity}} entities created within a date range.
        // /// </summary>
        // /// <param name="fromDate">The start date.</param>
        // /// <param name="toDate">The end date.</param>
        // /// <returns>A collection of {{entity}} entities.</returns>
        // Task<IEnumerable<{{entity}}>> GetByDateRangeAsync(DateTime fromDate, DateTime toDate);
        
        // /// <summary>
        // /// Gets {{entity}} entities by status.
        // /// </summary>
        // /// <param name="status">The status to filter by.</param>
        // /// <returns>A collection of {{entity}} entities.</returns>
        // Task<IEnumerable<{{entity}}>> GetByStatusAsync({{entity}}Status status);
        
        // /// <summary>
        // /// Gets a paged list of {{entity}} entities.
        // /// </summary>
        // /// <param name="pageNumber">The page number (1-based).</param>
        // /// <param name="pageSize">The number of items per page.</param>
        // /// <returns>A paged result of {{entity}} entities.</returns>
        // Task<PagedResult<{{entity}}>> GetPagedAsync(int pageNumber, int pageSize);
    }
}