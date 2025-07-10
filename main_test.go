package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestFindAllScaffoldDirs(t *testing.T) {
	// Create a temporary directory structure for testing
	tmpDir := t.TempDir()
	oldHome := os.Getenv("HOME")
	defer os.Setenv("HOME", oldHome)
	os.Setenv("HOME", tmpDir)

	// Create test directories
	localScaffold := ".scaffold"
	homeScaffold := filepath.Join(tmpDir, ".scaffold")
	configScaffold := filepath.Join(tmpDir, ".config", "scaffold")

	// Create directories
	os.MkdirAll(localScaffold, 0755)
	os.MkdirAll(homeScaffold, 0755)
	os.MkdirAll(configScaffold, 0755)

	tool := NewScaffoldTool()
	dirs := tool.findAllScaffoldDirs()

	// Should find all three directories
	if len(dirs) != 3 {
		t.Errorf("Expected 3 directories, got %d", len(dirs))
	}

	// Check order (closest to pwd first)
	if dirs[0] != localScaffold {
		t.Errorf("Expected first directory to be %s, got %s", localScaffold, dirs[0])
	}

	// Clean up
	os.RemoveAll(localScaffold)
}

func TestFindAllScaffoldDirsPartial(t *testing.T) {
	// Create a temporary directory structure for testing
	tmpDir := t.TempDir()
	oldHome := os.Getenv("HOME")
	defer os.Setenv("HOME", oldHome)
	os.Setenv("HOME", tmpDir)

	// Create only home scaffold directory
	homeScaffold := filepath.Join(tmpDir, ".scaffold")
	os.MkdirAll(homeScaffold, 0755)

	tool := NewScaffoldTool()
	dirs := tool.findAllScaffoldDirs()

	// Should find only one directory
	if len(dirs) != 1 {
		t.Errorf("Expected 1 directory, got %d", len(dirs))
	}

	if dirs[0] != homeScaffold {
		t.Errorf("Expected directory to be %s, got %s", homeScaffold, dirs[0])
	}
}

func TestFindTemplateFile(t *testing.T) {
	// Create a temporary directory structure for testing
	tmpDir := t.TempDir()
	oldHome := os.Getenv("HOME")
	defer os.Setenv("HOME", oldHome)
	os.Setenv("HOME", tmpDir)

	// Create test directories and files
	localScaffold := ".scaffold"
	homeScaffold := filepath.Join(tmpDir, ".scaffold")
	
	// Create directories
	os.MkdirAll(filepath.Join(localScaffold, "testcat", "templates"), 0755)
	os.MkdirAll(filepath.Join(homeScaffold, "testcat", "templates"), 0755)

	// Create template files
	localTemplate := filepath.Join(localScaffold, "testcat", "templates", "test.txt")
	homeTemplate := filepath.Join(homeScaffold, "testcat", "templates", "test.txt")
	
	os.WriteFile(localTemplate, []byte("local content"), 0644)
	os.WriteFile(homeTemplate, []byte("home content"), 0644)

	tool := NewScaffoldTool()
	foundPath := tool.findTemplateFile("testcat", "templates/test.txt")

	// Should find the local template (closer to pwd)
	if foundPath != localTemplate {
		t.Errorf("Expected template path to be %s, got %s", localTemplate, foundPath)
	}

	// Clean up
	os.RemoveAll(localScaffold)
}

func TestGetAvailableCategoriesIntegration(t *testing.T) {
	// Create a temporary directory structure for testing
	tmpDir := t.TempDir()
	oldHome := os.Getenv("HOME")
	defer os.Setenv("HOME", oldHome)
	os.Setenv("HOME", tmpDir)

	// Create test directories
	localScaffold := ".scaffold"
	homeScaffold := filepath.Join(tmpDir, ".scaffold")
	
	// Create category directories with config files
	os.MkdirAll(filepath.Join(localScaffold, "localcat"), 0755)
	os.MkdirAll(filepath.Join(homeScaffold, "homecat"), 0755)
	os.MkdirAll(filepath.Join(homeScaffold, "sharedcat"), 0755)
	os.MkdirAll(filepath.Join(localScaffold, "sharedcat"), 0755)
	
	// Create config files
	os.WriteFile(filepath.Join(localScaffold, "localcat", ".scaffold.toml"), []byte("[templates]"), 0644)
	os.WriteFile(filepath.Join(homeScaffold, "homecat", ".scaffold.toml"), []byte("[templates]"), 0644)
	os.WriteFile(filepath.Join(homeScaffold, "sharedcat", ".scaffold.toml"), []byte("[templates]"), 0644)
	os.WriteFile(filepath.Join(localScaffold, "sharedcat", ".scaffold.toml"), []byte("[templates]"), 0644)

	tool := NewScaffoldTool()
	categories, err := tool.getAvailableCategories()

	if err != nil {
		t.Fatalf("Error getting categories: %v", err)
	}

	// Should find all unique categories
	expectedCategories := map[string]bool{
		"localcat":  true,
		"homecat":   true,
		"sharedcat": true,
	}

	if len(categories) != len(expectedCategories) {
		t.Errorf("Expected %d categories, got %d", len(expectedCategories), len(categories))
	}

	for _, category := range categories {
		if !expectedCategories[category] {
			t.Errorf("Unexpected category: %s", category)
		}
	}

	// Clean up
	os.RemoveAll(localScaffold)
}