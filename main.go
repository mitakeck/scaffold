package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/BurntSushi/toml"
	"github.com/spf13/cobra"
)

type TemplateArg struct {
	Name        string `toml:"name"`
	Description string `toml:"description"`
	Default     string `toml:"default,omitempty"`
}

type TemplateFile struct {
	Source      string `toml:"source"`
	Destination string `toml:"destination"`
}

type Template struct {
	Description  string         `toml:"description"`
	RequiredArgs []TemplateArg  `toml:"required_args"`
	OptionalArgs []TemplateArg  `toml:"optional_args"`
	Files        []TemplateFile `toml:"files"`
}

type Config struct {
	Templates map[string]Template `toml:"templates"`
}

type ScaffoldTool struct {
	config       *Config
	configPath   string
	categoryPath string
}

func NewScaffoldTool() *ScaffoldTool {
	return &ScaffoldTool{}
}

func (s *ScaffoldTool) findScaffoldDir() (string, error) {
	searchPaths := []string{
		".scaffold",
		filepath.Join(os.Getenv("HOME"), ".scaffold"),
		filepath.Join(os.Getenv("HOME"), ".config", "scaffold"),
	}

	for _, path := range searchPaths {
		if stat, err := os.Stat(path); err == nil && stat.IsDir() {
			return path, nil
		}
	}

	return "", fmt.Errorf("no .scaffold directory found")
}

func (s *ScaffoldTool) getAvailableCategories() ([]string, error) {
	scaffoldDir, err := s.findScaffoldDir()
	if err != nil {
		return nil, err
	}

	entries, err := os.ReadDir(scaffoldDir)
	if err != nil {
		return nil, err
	}

	var categories []string
	for _, entry := range entries {
		if entry.IsDir() {
			configPath := filepath.Join(scaffoldDir, entry.Name(), ".scaffold.toml")
			if _, err := os.Stat(configPath); err == nil {
				categories = append(categories, entry.Name())
			}
		}
	}

	return categories, nil
}

func (s *ScaffoldTool) loadConfig(category string) error {
	scaffoldDir, err := s.findScaffoldDir()
	if err != nil {
		fmt.Println("Error: No .scaffold directory found")
		fmt.Println("Searched in:")
		fmt.Println("  - ./.scaffold")
		fmt.Println("  - ~/.scaffold")
		fmt.Println("  - ~/.config/scaffold")
		return err
	}

	categoryPath := filepath.Join(scaffoldDir, category)
	configPath := filepath.Join(categoryPath, ".scaffold.toml")

	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		fmt.Printf("Error: Category '%s' not found\n", category)
		categories, _ := s.getAvailableCategories()
		if len(categories) > 0 {
			fmt.Println("Available categories:")
			for _, cat := range categories {
				fmt.Printf("  %s\n", cat)
			}
		}
		return fmt.Errorf("category not found")
	}

	config := &Config{}
	if _, err := toml.DecodeFile(configPath, config); err != nil {
		return fmt.Errorf("error loading configuration: %v", err)
	}

	s.config = config
	s.configPath = configPath
	s.categoryPath = categoryPath
	return nil
}

func (s *ScaffoldTool) expandVariables(text string, variables map[string]string) string {
	now := time.Now()
	specialVars := map[string]string{
		"current_date":     now.Format("2006-01-02"),
		"current_time":     now.Format("15:04:05"),
		"current_datetime": now.Format("2006-01-02 15:04:05"),
	}

	for k, v := range variables {
		specialVars[k] = v
	}

	re := regexp.MustCompile(`\{\{(\w+)\}\}`)
	return re.ReplaceAllStringFunc(text, func(match string) string {
		varName := re.FindStringSubmatch(match)[1]
		if value, exists := specialVars[varName]; exists {
			return value
		}
		return match
	})
}

func (s *ScaffoldTool) generateTemplate(category, templateName string, args []string, kwargs map[string]string) error {
	if err := s.loadConfig(category); err != nil {
		return err
	}

	if s.config == nil || s.config.Templates == nil {
		return fmt.Errorf("no templates defined in configuration")
	}

	template, exists := s.config.Templates[templateName]
	if !exists {
		fmt.Printf("Error: Template '%s' not found in category '%s'\n", templateName, category)
		s.listTemplates(category)
		return fmt.Errorf("template not found")
	}

	if len(args) < len(template.RequiredArgs) {
		fmt.Printf("Error: Missing required arguments for template '%s'\n", templateName)
		argNames := make([]string, len(template.RequiredArgs))
		for i, arg := range template.RequiredArgs {
			argNames[i] = arg.Name
		}
		fmt.Printf("Required: %s\n", strings.Join(argNames, ", "))

		usage := make([]string, len(template.RequiredArgs))
		for i, arg := range template.RequiredArgs {
			usage[i] = "<" + arg.Name + ">"
		}
		fmt.Printf("Usage: scaffold %s %s %s [options]\n", category, templateName, strings.Join(usage, " "))
		return fmt.Errorf("missing required arguments")
	}

	variables := make(map[string]string)

	for i, arg := range template.RequiredArgs {
		variables[arg.Name] = args[i]
	}

	for _, arg := range template.OptionalArgs {
		if value, exists := kwargs[arg.Name]; exists {
			variables[arg.Name] = value
		} else {
			variables[arg.Name] = s.expandVariables(arg.Default, variables)
		}
	}

	for k, v := range kwargs {
		variables[k] = v
	}

	for _, file := range template.Files {
		sourcePath := filepath.Join(s.categoryPath, s.expandVariables(file.Source, variables))
		destPath := s.expandVariables(file.Destination, variables)

		if _, err := os.Stat(sourcePath); os.IsNotExist(err) {
			fmt.Printf("Error: Template file not found: %s\n", sourcePath)
			continue
		}

		if _, err := os.Stat(destPath); err == nil {
			fmt.Printf("File %s already exists. Overwrite? (y/n): ", destPath)
			reader := bufio.NewReader(os.Stdin)
			response, _ := reader.ReadString('\n')
			response = strings.TrimSpace(strings.ToLower(response))
			if response != "y" {
				fmt.Printf("Skipped: %s\n", destPath)
				continue
			}
		}

		if err := os.MkdirAll(filepath.Dir(destPath), 0755); err != nil {
			fmt.Printf("Error creating directory for %s: %v\n", destPath, err)
			continue
		}

		content, err := os.ReadFile(sourcePath)
		if err != nil {
			fmt.Printf("Error reading template file %s: %v\n", sourcePath, err)
			continue
		}

		expandedContent := s.expandVariables(string(content), variables)

		if err := os.WriteFile(destPath, []byte(expandedContent), 0644); err != nil {
			fmt.Printf("Error writing file %s: %v\n", destPath, err)
			continue
		}

		fmt.Printf("Generated: %s\n", destPath)
	}

	return nil
}

func (s *ScaffoldTool) listCategories() {
	categories, err := s.getAvailableCategories()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	if len(categories) == 0 {
		fmt.Println("No categories available")
		return
	}

	fmt.Println("Available categories:")
	for _, category := range categories {
		fmt.Printf("  %s\n", category)
	}
	fmt.Println("\nUsage: scaffold <category> <template> [args...]")
	fmt.Println("       scaffold <category> list")
	fmt.Println("       scaffold <category> info <template>")
}

func (s *ScaffoldTool) listTemplates(category string) {
	if err := s.loadConfig(category); err != nil {
		return
	}

	if s.config == nil || s.config.Templates == nil {
		fmt.Printf("No templates available in category '%s'\n", category)
		return
	}

	fmt.Printf("Available templates in '%s':\n", category)
	for name, template := range s.config.Templates {
		description := template.Description
		if description == "" {
			description = "No description"
		}
		fmt.Printf("  %s - %s\n", name, description)
	}
}

func (s *ScaffoldTool) showTemplateInfo(category, templateName string) {
	if err := s.loadConfig(category); err != nil {
		return
	}

	if s.config == nil || s.config.Templates == nil {
		fmt.Printf("No templates available in category '%s'\n", category)
		return
	}

	template, exists := s.config.Templates[templateName]
	if !exists {
		fmt.Printf("Template '%s' not found in category '%s'\n", templateName, category)
		return
	}

	fmt.Printf("Template: %s.%s\n", category, templateName)
	description := template.Description
	if description == "" {
		description = "No description"
	}
	fmt.Printf("Description: %s\n", description)

	if len(template.RequiredArgs) > 0 {
		fmt.Println("\nRequired arguments:")
		for _, arg := range template.RequiredArgs {
			fmt.Printf("  %s - %s\n", arg.Name, arg.Description)
		}
	}

	if len(template.OptionalArgs) > 0 {
		fmt.Println("\nOptional arguments:")
		for _, arg := range template.OptionalArgs {
			defaultValue := arg.Default
			if defaultValue == "" {
				defaultValue = ""
			}
			fmt.Printf("  %s (default: %s) - %s\n", arg.Name, defaultValue, arg.Description)
		}
	}

	if len(template.Files) > 0 {
		fmt.Println("\nGenerated files:")
		for _, file := range template.Files {
			fmt.Printf("  %s\n", file.Destination)
		}
	}

	usage := make([]string, len(template.RequiredArgs))
	for i, arg := range template.RequiredArgs {
		usage[i] = "<" + arg.Name + ">"
	}
	fmt.Printf("\nUsage: scaffold %s %s %s [key=value...]\n", category, templateName, strings.Join(usage, " "))
}

func parseKeyValue(args []string) ([]string, map[string]string) {
	var positional []string
	kwargs := make(map[string]string)

	for _, arg := range args {
		if strings.Contains(arg, "=") {
			parts := strings.SplitN(arg, "=", 2)
			kwargs[parts[0]] = parts[1]
		} else {
			positional = append(positional, arg)
		}
	}

	return positional, kwargs
}

func main() {
	tool := NewScaffoldTool()

	var rootCmd = &cobra.Command{
		Use:   "scaffold",
		Short: "Universal Scaffold Tool",
		Long:  "A universal scaffolding tool for generating code from templates",
		RunE: func(cmd *cobra.Command, args []string) error {
			if len(args) == 0 {
				tool.listCategories()
				return nil
			}

			category := args[0]
			if len(args) == 1 {
				tool.listTemplates(category)
				return nil
			}

			subcommand := args[1]
			switch subcommand {
			case "list":
				tool.listTemplates(category)
				return nil
			case "info":
				if len(args) < 3 {
					fmt.Printf("Usage: scaffold %s info <template>\n", category)
					return fmt.Errorf("missing template name")
				}
				tool.showTemplateInfo(category, args[2])
				return nil
			default:
				// Treat as template generation
				templateName := subcommand
				remainingArgs := args[2:]
				positional, kwargs := parseKeyValue(remainingArgs)
				return tool.generateTemplate(category, templateName, positional, kwargs)
			}
		},
	}

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
