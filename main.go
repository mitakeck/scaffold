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
	config     *Config
	configPath string
}

func NewScaffoldTool() *ScaffoldTool {
	return &ScaffoldTool{}
}

func (s *ScaffoldTool) findConfigFile() (string, error) {
	searchPaths := []string{
		".scaffold.toml",
		filepath.Join(os.Getenv("HOME"), ".scaffold.toml"),
		filepath.Join(os.Getenv("HOME"), ".config", "scaffold", ".scaffold.toml"),
	}

	for _, path := range searchPaths {
		if _, err := os.Stat(path); err == nil {
			return path, nil
		}
	}

	return "", fmt.Errorf("no .scaffold.toml configuration file found")
}

func (s *ScaffoldTool) loadConfig() error {
	configPath, err := s.findConfigFile()
	if err != nil {
		fmt.Println("Error: No .scaffold.toml configuration file found")
		fmt.Println("Searched in:")
		fmt.Println("  - ./.scaffold.toml")
		fmt.Println("  - ~/.scaffold.toml")
		fmt.Println("  - ~/.config/scaffold/.scaffold.toml")
		return err
	}

	config := &Config{}
	if _, err := toml.DecodeFile(configPath, config); err != nil {
		return fmt.Errorf("error loading configuration: %v", err)
	}

	s.config = config
	s.configPath = configPath
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

func (s *ScaffoldTool) generateTemplate(templateName string, args []string, kwargs map[string]string) error {
	if s.config == nil || s.config.Templates == nil {
		return fmt.Errorf("no templates defined in configuration")
	}

	template, exists := s.config.Templates[templateName]
	if !exists {
		fmt.Printf("Error: Template '%s' not found\n", templateName)
		s.listTemplates()
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
		fmt.Printf("Usage: scaffold generate %s %s [options]\n", templateName, strings.Join(usage, " "))
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

	configDir := filepath.Dir(s.configPath)

	for _, file := range template.Files {
		sourcePath := filepath.Join(configDir, file.Source)
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

func (s *ScaffoldTool) listTemplates() {
	if s.config == nil || s.config.Templates == nil {
		fmt.Println("No templates available")
		return
	}

	fmt.Println("Available templates:")
	for name, template := range s.config.Templates {
		description := template.Description
		if description == "" {
			description = "No description"
		}
		fmt.Printf("  %s - %s\n", name, description)
	}
}

func (s *ScaffoldTool) showTemplateInfo(templateName string) {
	if s.config == nil || s.config.Templates == nil {
		fmt.Println("No templates available")
		return
	}

	template, exists := s.config.Templates[templateName]
	if !exists {
		fmt.Printf("Template '%s' not found\n", templateName)
		return
	}

	fmt.Printf("Template: %s\n", templateName)
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
	}

	var generateCmd = &cobra.Command{
		Use:   "generate [template] [args...] [key=value...]",
		Short: "Generate files from template",
		Args:  cobra.MinimumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := tool.loadConfig(); err != nil {
				return err
			}

			templateName := args[0]
			remainingArgs := args[1:]
			positional, kwargs := parseKeyValue(remainingArgs)

			return tool.generateTemplate(templateName, positional, kwargs)
		},
	}

	var listCmd = &cobra.Command{
		Use:   "list",
		Short: "List available templates",
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := tool.loadConfig(); err != nil {
				return err
			}
			tool.listTemplates()
			return nil
		},
	}

	var infoCmd = &cobra.Command{
		Use:   "info [template]",
		Short: "Show template information",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := tool.loadConfig(); err != nil {
				return err
			}
			tool.showTemplateInfo(args[0])
			return nil
		},
	}

	rootCmd.AddCommand(generateCmd)
	rootCmd.AddCommand(listCmd)
	rootCmd.AddCommand(infoCmd)

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
