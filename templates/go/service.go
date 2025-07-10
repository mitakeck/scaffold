package {{package}}

import (
	"context"
	"fmt"
)

// {{name}}Service represents the service interface
// Author: {{author}}
// Created: {{date}}
type {{name}}Service interface {
	Create(ctx context.Context, data interface{}) error
	GetByID(ctx context.Context, id string) (interface{}, error)
	Update(ctx context.Context, id string, data interface{}) error
	Delete(ctx context.Context, id string) error
	List(ctx context.Context) ([]interface{}, error)
}

// {{name}}ServiceImpl implements {{name}}Service
type {{name}}ServiceImpl struct {
	// Add dependencies here (e.g., repository, logger, etc.)
}

// New{{name}}Service creates a new instance of {{name}}Service
func New{{name}}Service() {{name}}Service {
	return &{{name}}ServiceImpl{
		// Initialize dependencies here
	}
}

// Create creates a new {{name}} entity
func (s *{{name}}ServiceImpl) Create(ctx context.Context, data interface{}) error {
	// TODO: Implement create logic
	return fmt.Errorf("not implemented")
}

// GetByID retrieves a {{name}} entity by ID
func (s *{{name}}ServiceImpl) GetByID(ctx context.Context, id string) (interface{}, error) {
	// TODO: Implement get by ID logic
	return nil, fmt.Errorf("not implemented")
}

// Update updates an existing {{name}} entity
func (s *{{name}}ServiceImpl) Update(ctx context.Context, id string, data interface{}) error {
	// TODO: Implement update logic
	return fmt.Errorf("not implemented")
}

// Delete deletes a {{name}} entity by ID
func (s *{{name}}ServiceImpl) Delete(ctx context.Context, id string) error {
	// TODO: Implement delete logic
	return fmt.Errorf("not implemented")
}

// List retrieves all {{name}} entities
func (s *{{name}}ServiceImpl) List(ctx context.Context) ([]interface{}, error) {
	// TODO: Implement list logic
	return nil, fmt.Errorf("not implemented")
}