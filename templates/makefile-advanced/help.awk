#!/usr/bin/awk -f
# help.awk - Advanced Makefile help formatter
# Author: {{author}}
# Created: {{date}}
# Based on: https://zenn.dev/loglass/articles/0016-make-makefile

BEGIN {
    # Color definitions
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # State variables
    current_section = ""
    max_command_length = 0
    
    # Arrays to store commands and descriptions
    delete commands
    delete descriptions
    delete sections
    command_count = 0
}

# Match section headers (## Section Name ##)
/^[[:space:]]*## .* ##[[:space:]]*$/ {
    gsub(/^[[:space:]]*## /, "", $0)
    gsub(/ ##[[:space:]]*$/, "", $0)
    current_section = $0
    next
}

# Match command definitions with descriptions
/^[a-zA-Z_-]+:.*##/ {
    # Extract command name and description
    match($0, /^([a-zA-Z_-]+):.*## (.*)$/, matches)
    if (matches[1] && matches[2]) {
        command = matches[1]
        description = matches[2]
        
        # Store command info
        commands[command_count] = command
        descriptions[command] = description
        sections[command] = current_section
        command_count++
        
        # Track max command length for alignment
        if (length(command) > max_command_length) {
            max_command_length = length(command)
        }
    }
}

END {
    # Group commands by section
    delete section_commands
    for (i = 0; i < command_count; i++) {
        cmd = commands[i]
        sec = sections[cmd]
        if (sec == "") sec = "General"
        
        if (!(sec in section_commands)) {
            section_commands[sec] = ""
        }
        section_commands[sec] = section_commands[sec] cmd "\n"
    }
    
    # Print sections in order
    section_order[0] = "Development Environment"
    section_order[1] = "Docker Tasks"
    section_order[2] = "Node.js Tasks"
    section_order[3] = "Go Tasks"
    section_order[4] = "Python Tasks"
    section_order[5] = "Testing"
    section_order[6] = "Code Quality"
    section_order[7] = "Build and Release"
    section_order[8] = "Database"
    section_order[9] = "Monitoring and Logs"
    section_order[10] = "Help"
    section_order[11] = "General"
    
    # Print each section
    for (i = 0; i <= 11; i++) {
        section = section_order[i]
        if (section in section_commands) {
            print_section(section)
        }
    }
    
    # Print any remaining sections not in the predefined order
    for (sec in section_commands) {
        found = 0
        for (i = 0; i <= 11; i++) {
            if (section_order[i] == sec) {
                found = 1
                break
            }
        }
        if (!found) {
            print_section(sec)
        }
    }
    
    # Print footer
    print ""
    print DIM "Usage examples:" RESET
    print DIM "  make init          # Initialize development environment" RESET
    print DIM "  make test          # Run all tests" RESET
    print DIM "  make check         # Run quality checks and tests" RESET
    print DIM "  make build         # Build the project" RESET
    print DIM "  make help-simple   # Show simple help without colors" RESET
}

function print_section(section) {
    if (section_commands[section] == "") return
    
    print ""
    print BOLD CYAN "▶ " section RESET
    print ""
    
    # Split commands and print each one
    split(section_commands[section], cmd_list, "\n")
    for (j in cmd_list) {
        cmd = cmd_list[j]
        if (cmd == "") continue
        
        desc = descriptions[cmd]
        padding = ""
        for (k = length(cmd); k < max_command_length + 2; k++) {
            padding = padding " "
        }
        
        # Color command names based on their purpose
        cmd_color = get_command_color(cmd)
        print "  " cmd_color cmd RESET padding DIM desc RESET
    }
}

function get_command_color(cmd) {
    if (match(cmd, /^(init|setup|install)$/)) return GREEN
    if (match(cmd, /^(clean|remove|delete)$/)) return RED
    if (match(cmd, /^(test|check|lint|format)$/)) return YELLOW
    if (match(cmd, /^(build|release|deploy)$/)) return CYAN
    if (match(cmd, /^(help|status|logs)$/)) return DIM
    return ""
}