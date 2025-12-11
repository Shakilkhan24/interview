# Go Programming Basics for DevOps Engineers
## Learn Go Fundamentals and Build Practical DevOps Tools

---

## Table of Contents

### Part I: Go Basics
1. [Getting Started](#1-getting-started)
2. [Variables & Types](#2-variables--types)
3. [Functions](#3-functions)
4. [Control Structures](#4-control-structures)
5. [Arrays, Slices & Maps](#5-arrays-slices--maps)
6. [Structs & Methods](#6-structs--methods)
7. [Interfaces](#7-interfaces)
8. [Error Handling](#8-error-handling)
9. [Goroutines & Channels](#9-goroutines--channels)
10. [Packages & Modules](#10-packages--modules)

### Part II: DevOps Projects
11. [CLI Tool - System Info](#11-cli-tool---system-info)
12. [File Operations - Log Parser](#12-file-operations---log-parser)
13. [HTTP Client - API Health Checker](#13-http-client---api-health-checker)
14. [HTTP Server - Simple Metrics Endpoint](#14-http-server---simple-metrics-endpoint)
15. [JSON Processing - Config Validator](#15-json-processing---config-validator)
16. [YAML Processing - Kubernetes Manifest Reader](#16-yaml-processing---kubernetes-manifest-reader)
17. [Concurrent Tasks - Multi-Server Health Check](#17-concurrent-tasks---multi-server-health-check)
18. [File Watcher - Auto-Reload Config](#18-file-watcher---auto-reload-config)

---

## Part I: Go Basics

### 1. Getting Started

#### 1.1 Installation

**Linux/macOS:**
```bash
# Download from https://go.dev/dl/
# Or use package manager

# macOS
brew install go

# Ubuntu/Debian
sudo apt-get install golang-go

# Verify
go version
```

**Windows:**
- Download installer from https://go.dev/dl/
- Run installer
- Verify: `go version`

#### 1.2 Your First Program

**Create `hello.go`:**
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, DevOps World!")
}
```

**Run:**
```bash
go run hello.go
# Output: Hello, DevOps World!
```

**Build executable:**
```bash
go build hello.go
./hello  # Linux/macOS
hello.exe  # Windows
```

#### 1.3 Go Workspace

```bash
# Create project directory
mkdir my-go-project
cd my-go-project

# Initialize Go module
go mod init my-go-project

# This creates go.mod file
```

---

### 2. Variables & Types

#### 2.1 Basic Types

```go
package main

import "fmt"

func main() {
    // Strings
    var name string = "DevOps Engineer"
    name2 := "Go Developer"  // Short declaration
    
    // Integers
    var age int = 30
    count := 42
    
    // Floats
    var price float64 = 99.99
    temperature := 25.5
    
    // Booleans
    var isActive bool = true
    enabled := false
    
    // Print
    fmt.Println(name, name2)
    fmt.Println(age, count)
    fmt.Println(price, temperature)
    fmt.Println(isActive, enabled)
}
```

#### 2.2 Type Inference

```go
package main

import "fmt"

func main() {
    // Go infers types
    name := "John"        // string
    age := 30             // int
    salary := 5000.50     // float64
    active := true        // bool
    
    fmt.Printf("Name: %s, Age: %d, Salary: %.2f, Active: %t\n", 
        name, age, salary, active)
}
```

#### 2.3 Constants

```go
package main

import "fmt"

const (
    API_URL = "https://api.example.com"
    TIMEOUT = 30
    MAX_RETRIES = 3
)

func main() {
    fmt.Println("API URL:", API_URL)
    fmt.Println("Timeout:", TIMEOUT, "seconds")
    fmt.Println("Max Retries:", MAX_RETRIES)
}
```

---

### 3. Functions

#### 3.1 Basic Functions

```go
package main

import "fmt"

// Simple function
func greet(name string) {
    fmt.Printf("Hello, %s!\n", name)
}

// Function with return value
func add(a, b int) int {
    return a + b
}

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}

func main() {
    greet("DevOps Engineer")
    
    sum := add(10, 20)
    fmt.Println("Sum:", sum)
    
    result, err := divide(10, 2)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result)
    }
}
```

#### 3.2 Named Return Values

```go
package main

import "fmt"

func calculate(a, b int) (sum int, product int, difference int) {
    sum = a + b
    product = a * b
    difference = a - b
    return  // Naked return
}

func main() {
    s, p, d := calculate(10, 5)
    fmt.Printf("Sum: %d, Product: %d, Difference: %d\n", s, p, d)
}
```

#### 3.3 Variadic Functions

```go
package main

import "fmt"

// Accepts variable number of arguments
func sum(numbers ...int) int {
    total := 0
    for _, num := range numbers {
        total += num
    }
    return total
}

func main() {
    fmt.Println(sum(1, 2, 3))           // 6
    fmt.Println(sum(1, 2, 3, 4, 5))     // 15
    fmt.Println(sum())                  // 0
}
```

---

### 4. Control Structures

#### 4.1 If/Else

```go
package main

import "fmt"

func checkStatus(statusCode int) {
    if statusCode >= 200 && statusCode < 300 {
        fmt.Println("Success")
    } else if statusCode >= 400 && statusCode < 500 {
        fmt.Println("Client Error")
    } else if statusCode >= 500 {
        fmt.Println("Server Error")
    } else {
        fmt.Println("Unknown Status")
    }
}

// If with initialization
func checkFile(filename string) {
    if content, err := readFile(filename); err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Content:", content)
    }
}

func readFile(filename string) (string, error) {
    // Simulated
    return "file content", nil
}

func main() {
    checkStatus(200)
    checkStatus(404)
    checkStatus(500)
}
```

#### 4.2 Switch

```go
package main

import "fmt"

func getStatusMessage(code int) string {
    switch code {
    case 200:
        return "OK"
    case 404:
        return "Not Found"
    case 500:
        return "Internal Server Error"
    default:
        return "Unknown"
    }
}

// Switch without condition (like if/else chain)
func checkTime(hour int) {
    switch {
    case hour < 12:
        fmt.Println("Good morning")
    case hour < 18:
        fmt.Println("Good afternoon")
    default:
        fmt.Println("Good evening")
    }
}

func main() {
    fmt.Println(getStatusMessage(200))
    checkTime(14)
}
```

#### 4.3 For Loops

```go
package main

import "fmt"

func main() {
    // Traditional for loop
    for i := 0; i < 5; i++ {
        fmt.Println("Iteration", i)
    }
    
    // While-style loop
    count := 0
    for count < 3 {
        fmt.Println("Count:", count)
        count++
    }
    
    // Infinite loop (with break)
    i := 0
    for {
        if i >= 3 {
            break
        }
        fmt.Println("Infinite loop iteration", i)
        i++
    }
    
    // Range over slice
    servers := []string{"server1", "server2", "server3"}
    for index, server := range servers {
        fmt.Printf("Index %d: %s\n", index, server)
    }
    
    // Range (index only)
    for i := range servers {
        fmt.Println("Index:", i)
    }
    
    // Range (value only)
    for _, server := range servers {
        fmt.Println("Server:", server)
    }
}
```

---

### 5. Arrays, Slices & Maps

#### 5.1 Arrays & Slices

```go
package main

import "fmt"

func main() {
    // Array (fixed size)
    var arr [3]string
    arr[0] = "server1"
    arr[1] = "server2"
    arr[2] = "server3"
    
    // Slice (dynamic size) - more common
    servers := []string{"server1", "server2"}
    
    // Append to slice
    servers = append(servers, "server3")
    servers = append(servers, "server4", "server5")
    
    // Slice operations
    fmt.Println("Length:", len(servers))
    fmt.Println("Capacity:", cap(servers))
    fmt.Println("First:", servers[0])
    fmt.Println("Last:", servers[len(servers)-1])
    
    // Slice a slice
    firstTwo := servers[:2]
    lastTwo := servers[3:]
    middle := servers[1:3]
    
    fmt.Println("First two:", firstTwo)
    fmt.Println("Last two:", lastTwo)
    fmt.Println("Middle:", middle)
    
    // Make slice with capacity
    numbers := make([]int, 0, 10)  // length 0, capacity 10
    numbers = append(numbers, 1, 2, 3)
}
```

#### 5.2 Maps

```go
package main

import "fmt"

func main() {
    // Create map
    config := make(map[string]string)
    config["database_url"] = "postgres://localhost/db"
    config["api_key"] = "secret123"
    
    // Map literal
    servers := map[string]int{
        "server1": 8080,
        "server2": 8081,
        "server3": 8082,
    }
    
    // Access values
    fmt.Println("Database URL:", config["database_url"])
    fmt.Println("Server1 port:", servers["server1"])
    
    // Check if key exists
    if port, exists := servers["server1"]; exists {
        fmt.Println("Server1 port:", port)
    }
    
    // Delete key
    delete(servers, "server2")
    
    // Iterate map
    for key, value := range config {
        fmt.Printf("%s: %s\n", key, value)
    }
    
    // Map length
    fmt.Println("Config entries:", len(config))
}
```

---

### 6. Structs & Methods

#### 6.1 Structs

```go
package main

import "fmt"

// Define struct
type Server struct {
    Name     string
    IP       string
    Port     int
    Status   string
}

// Method on struct
func (s Server) GetAddress() string {
    return fmt.Sprintf("%s:%d", s.IP, s.Port)
}

// Method with pointer receiver (can modify)
func (s *Server) UpdateStatus(status string) {
    s.Status = status
}

func main() {
    // Create struct
    server1 := Server{
        Name:   "web-server",
        IP:     "192.168.1.10",
        Port:   8080,
        Status: "running",
    }
    
    // Access fields
    fmt.Println("Server:", server1.Name)
    fmt.Println("Address:", server1.GetAddress())
    
    // Update status
    server1.UpdateStatus("maintenance")
    fmt.Println("New status:", server1.Status)
    
    // Pointer to struct
    server2 := &Server{
        Name: "db-server",
        IP:   "192.168.1.20",
        Port: 5432,
    }
    server2.UpdateStatus("running")
    fmt.Println("Server2:", server2.Name, server2.Status)
}
```

#### 6.2 Embedded Structs

```go
package main

import "fmt"

type Address struct {
    Street string
    City   string
    Zip    string
}

type Server struct {
    Name    string
    Address Address  // Embedded
}

func main() {
    server := Server{
        Name: "web-server",
        Address: Address{
            Street: "123 Main St",
            City:   "San Francisco",
            Zip:    "94102",
        },
    }
    
    fmt.Println("Server:", server.Name)
    fmt.Println("City:", server.Address.City)
}
```

---

### 7. Interfaces

#### 7.1 Basic Interfaces

```go
package main

import "fmt"

// Interface definition
type HealthChecker interface {
    Check() bool
    GetName() string
}

// Struct implementing interface
type Server struct {
    Name   string
    Status string
}

func (s Server) Check() bool {
    return s.Status == "healthy"
}

func (s Server) GetName() string {
    return s.Name
}

// Another struct implementing same interface
type Database struct {
    Name   string
    Online bool
}

func (d Database) Check() bool {
    return d.Online
}

func (d Database) GetName() string {
    return d.Name
}

// Function accepting interface
func checkHealth(hc HealthChecker) {
    if hc.Check() {
        fmt.Printf("%s is healthy\n", hc.GetName())
    } else {
        fmt.Printf("%s is unhealthy\n", hc.GetName())
    }
}

func main() {
    server := Server{Name: "web-server", Status: "healthy"}
    db := Database{Name: "postgres", Online: true}
    
    checkHealth(server)
    checkHealth(db)
}
```

---

### 8. Error Handling

#### 8.1 Error Basics

```go
package main

import (
    "errors"
    "fmt"
)

// Function returning error
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Custom error
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

func validateConfig(port int) error {
    if port < 1 || port > 65535 {
        return ValidationError{
            Field:   "port",
            Message: "must be between 1 and 65535",
        }
    }
    return nil
}

func main() {
    // Check error
    result, err := divide(10, 2)
    if err != nil {
        fmt.Println("Error:", err)
    } else {
        fmt.Println("Result:", result)
    }
    
    // Error check
    if err := validateConfig(70000); err != nil {
        fmt.Println("Validation error:", err)
    }
}
```

#### 8.2 Error Wrapping

```go
package main

import (
    "errors"
    "fmt"
)

func readConfig() error {
    return errors.New("file not found")
}

func loadConfig() error {
    err := readConfig()
    if err != nil {
        return fmt.Errorf("failed to load config: %w", err)
    }
    return nil
}

func main() {
    err := loadConfig()
    if err != nil {
        fmt.Println("Error:", err)
        // Check if underlying error
        if errors.Is(err, errors.New("file not found")) {
            fmt.Println("Original error found")
        }
    }
}
```

---

### 9. Goroutines & Channels

#### 9.1 Goroutines

```go
package main

import (
    "fmt"
    "time"
)

func checkServer(name string) {
    fmt.Printf("Checking %s...\n", name)
    time.Sleep(1 * time.Second)
    fmt.Printf("%s is healthy\n", name)
}

func main() {
    // Sequential execution
    checkServer("server1")
    checkServer("server2")
    
    // Concurrent execution with goroutines
    go checkServer("server3")
    go checkServer("server4")
    
    // Wait for goroutines to finish
    time.Sleep(2 * time.Second)
    fmt.Println("All checks complete")
}
```

#### 9.2 Channels

```go
package main

import (
    "fmt"
    "time"
)

func checkServer(name string, ch chan string) {
    fmt.Printf("Checking %s...\n", name)
    time.Sleep(1 * time.Second)
    ch <- fmt.Sprintf("%s is healthy", name)
}

func main() {
    // Create channel
    ch := make(chan string)
    
    // Start goroutines
    go checkServer("server1", ch)
    go checkServer("server2", ch)
    go checkServer("server3", ch)
    
    // Receive messages
    for i := 0; i < 3; i++ {
        msg := <-ch
        fmt.Println(msg)
    }
}
```

#### 9.3 Select Statement

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)
    
    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "Message from channel 1"
    }()
    
    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "Message from channel 2"
    }()
    
    // Select waits for first available channel
    select {
    case msg1 := <-ch1:
        fmt.Println("Received:", msg1)
    case msg2 := <-ch2:
        fmt.Println("Received:", msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout")
    }
}
```

---

### 10. Packages & Modules

#### 10.1 Creating a Module

```bash
# Create project
mkdir myproject
cd myproject
go mod init myproject
```

**main.go:**
```go
package main

import (
    "fmt"
    "myproject/utils"
)

func main() {
    result := utils.Add(10, 20)
    fmt.Println("Result:", result)
}
```

**utils/math.go:**
```go
package utils

func Add(a, b int) int {
    return a + b
}

func Multiply(a, b int) int {
    return a * b
}
```

**Run:**
```bash
go run main.go
```

#### 10.2 Using External Packages

```go
package main

import (
    "fmt"
    "github.com/fatih/color"
)

func main() {
    color.Red("This is red text")
    color.Green("This is green text")
    color.Blue("This is blue text")
}
```

**Install dependency:**
```bash
go get github.com/fatih/color
go mod tidy
```

---

## Part II: DevOps Projects

### 11. CLI Tool - System Info

**Create `systeminfo.go`:**
```go
package main

import (
    "fmt"
    "os"
    "os/exec"
    "runtime"
)

func main() {
    fmt.Println("=== System Information ===")
    
    // OS Info
    fmt.Printf("OS: %s\n", runtime.GOOS)
    fmt.Printf("Architecture: %s\n", runtime.GOARCH)
    fmt.Printf("Go Version: %s\n", runtime.Version())
    fmt.Printf("CPU Cores: %d\n", runtime.NumCPU())
    
    // Hostname
    hostname, _ := os.Hostname()
    fmt.Printf("Hostname: %s\n", hostname)
    
    // Environment variables
    fmt.Println("\n=== Environment Variables ===")
    fmt.Printf("USER: %s\n", os.Getenv("USER"))
    fmt.Printf("HOME: %s\n", os.Getenv("HOME"))
    fmt.Printf("PATH: %s\n", os.Getenv("PATH"))
    
    // System commands (Linux/macOS)
    if runtime.GOOS != "windows" {
        fmt.Println("\n=== Uptime ===")
        cmd := exec.Command("uptime")
        output, _ := cmd.Output()
        fmt.Print(string(output))
    }
}
```

**Run:**
```bash
go run systeminfo.go
```

---

### 12. File Operations - Log Parser

**Create `logparser.go`:**
```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "strings"
)

func parseLogFile(filename string) error {
    file, err := os.Open(filename)
    if err != nil {
        return fmt.Errorf("error opening file: %w", err)
    }
    defer file.Close()
    
    scanner := bufio.NewScanner(file)
    errorCount := 0
    warningCount := 0
    infoCount := 0
    
    for scanner.Scan() {
        line := scanner.Text()
        lineLower := strings.ToLower(line)
        
        if strings.Contains(lineLower, "error") {
            errorCount++
            fmt.Printf("[ERROR] %s\n", line)
        } else if strings.Contains(lineLower, "warning") {
            warningCount++
            fmt.Printf("[WARNING] %s\n", line)
        } else if strings.Contains(lineLower, "info") {
            infoCount++
        }
    }
    
    if err := scanner.Err(); err != nil {
        return fmt.Errorf("error reading file: %w", err)
    }
    
    fmt.Printf("\n=== Summary ===\n")
    fmt.Printf("Errors: %d\n", errorCount)
    fmt.Printf("Warnings: %d\n", warningCount)
    fmt.Printf("Info: %d\n", infoCount)
    
    return nil
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run logparser.go <logfile>")
        os.Exit(1)
    }
    
    filename := os.Args[1]
    if err := parseLogFile(filename); err != nil {
        fmt.Printf("Error: %v\n", err)
        os.Exit(1)
    }
}
```

**Create sample log file `app.log`:**
```
2024-01-15 10:00:00 INFO Application started
2024-01-15 10:01:00 WARNING High memory usage
2024-01-15 10:02:00 ERROR Database connection failed
2024-01-15 10:03:00 INFO Connection restored
2024-01-15 10:04:00 ERROR File not found
```

**Run:**
```bash
go run logparser.go app.log
```

---

### 13. HTTP Client - API Health Checker

**Create `healthcheck.go`:**
```go
package main

import (
    "fmt"
    "net/http"
    "time"
)

type Server struct {
    Name    string
    URL     string
    Status  string
    Latency time.Duration
}

func checkHealth(name, url string) Server {
    start := time.Now()
    
    client := http.Client{
        Timeout: 5 * time.Second,
    }
    
    resp, err := client.Get(url)
    latency := time.Since(start)
    
    server := Server{
        Name:    name,
        URL:     url,
        Latency: latency,
    }
    
    if err != nil {
        server.Status = "DOWN"
        return server
    }
    defer resp.Body.Close()
    
    if resp.StatusCode >= 200 && resp.StatusCode < 300 {
        server.Status = "UP"
    } else {
        server.Status = "DEGRADED"
    }
    
    return server
}

func main() {
    servers := []struct {
        name string
        url  string
    }{
        {"Google", "https://www.google.com"},
        {"GitHub", "https://www.github.com"},
        {"Local API", "http://localhost:8080/health"},
    }
    
    fmt.Println("=== Health Check Results ===\n")
    
    for _, s := range servers {
        result := checkHealth(s.name, s.url)
        fmt.Printf("Server: %s\n", result.Name)
        fmt.Printf("URL: %s\n", result.URL)
        fmt.Printf("Status: %s\n", result.Status)
        fmt.Printf("Latency: %v\n", result.Latency)
        fmt.Println("---")
    }
}
```

**Run:**
```bash
go run healthcheck.go
```

---

### 14. HTTP Server - Simple Metrics Endpoint

**Create `metrics-server.go`:**
```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "runtime"
    "time"
)

type Metrics struct {
    Timestamp    string  `json:"timestamp"`
    Uptime       string  `json:"uptime"`
    GoVersion    string  `json:"go_version"`
    NumGoroutine int     `json:"num_goroutines"`
    NumCPU       int     `json:"num_cpu"`
    Memory       Memory  `json:"memory"`
}

type Memory struct {
    Alloc      uint64 `json:"alloc"`
    TotalAlloc uint64 `json:"total_alloc"`
    Sys        uint64 `json:"sys"`
    NumGC      uint32 `json:"num_gc"`
}

var startTime = time.Now()

func metricsHandler(w http.ResponseWriter, r *http.Request) {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    
    metrics := Metrics{
        Timestamp:    time.Now().Format(time.RFC3339),
        Uptime:       time.Since(startTime).String(),
        GoVersion:    runtime.Version(),
        NumGoroutine: runtime.NumGoroutine(),
        NumCPU:       runtime.NumCPU(),
        Memory: Memory{
            Alloc:      m.Alloc,
            TotalAlloc: m.TotalAlloc,
            Sys:        m.Sys,
            NumGC:      m.NumGC,
        },
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(metrics)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, "OK")
}

func main() {
    http.HandleFunc("/metrics", metricsHandler)
    http.HandleFunc("/health", healthHandler)
    
    fmt.Println("Server starting on :8080")
    fmt.Println("Metrics: http://localhost:8080/metrics")
    fmt.Println("Health: http://localhost:8080/health")
    
    if err := http.ListenAndServe(":8080", nil); err != nil {
        fmt.Printf("Server error: %v\n", err)
    }
}
```

**Run:**
```bash
go run metrics-server.go

# In another terminal:
curl http://localhost:8080/metrics
curl http://localhost:8080/health
```

---

### 15. JSON Processing - Config Validator

**Create `config-validator.go`:**
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type Config struct {
    Server   ServerConfig   `json:"server"`
    Database DatabaseConfig `json:"database"`
    Logging  LoggingConfig  `json:"logging"`
}

type ServerConfig struct {
    Host string `json:"host"`
    Port int    `json:"port"`
}

type DatabaseConfig struct {
    Host     string `json:"host"`
    Port     int    `json:"port"`
    Database string `json:"database"`
    Username string `json:"username"`
}

type LoggingConfig struct {
    Level  string `json:"level"`
    Format string `json:"format"`
}

func validateConfig(config Config) []string {
    var errors []string
    
    if config.Server.Host == "" {
        errors = append(errors, "server.host is required")
    }
    if config.Server.Port < 1 || config.Server.Port > 65535 {
        errors = append(errors, "server.port must be between 1 and 65535")
    }
    if config.Database.Host == "" {
        errors = append(errors, "database.host is required")
    }
    if config.Database.Database == "" {
        errors = append(errors, "database.database is required")
    }
    if config.Logging.Level == "" {
        errors = append(errors, "logging.level is required")
    }
    
    return errors
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run config-validator.go <config.json>")
        os.Exit(1)
    }
    
    filename := os.Args[1]
    data, err := os.ReadFile(filename)
    if err != nil {
        fmt.Printf("Error reading file: %v\n", err)
        os.Exit(1)
    }
    
    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        fmt.Printf("Error parsing JSON: %v\n", err)
        os.Exit(1)
    }
    
    errors := validateConfig(config)
    if len(errors) > 0 {
        fmt.Println("Validation errors:")
        for _, err := range errors {
            fmt.Printf("  - %s\n", err)
        }
        os.Exit(1)
    }
    
    fmt.Println("Config is valid!")
    fmt.Printf("Server: %s:%d\n", config.Server.Host, config.Server.Port)
    fmt.Printf("Database: %s/%s\n", config.Database.Host, config.Database.Database)
}
```

**Create `config.json`:**
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "username": "admin"
  },
  "logging": {
    "level": "info",
    "format": "json"
  }
}
```

**Run:**
```bash
go run config-validator.go config.json
```

---

### 16. YAML Processing - Kubernetes Manifest Reader

**First, install YAML library:**
```bash
go get gopkg.in/yaml.v3
```

**Create `k8s-reader.go`:**
```go
package main

import (
    "fmt"
    "os"
    "gopkg.in/yaml.v3"
)

type Deployment struct {
    APIVersion string `yaml:"apiVersion"`
    Kind       string `yaml:"kind"`
    Metadata   struct {
        Name      string `yaml:"name"`
        Namespace string `yaml:"namespace"`
    } `yaml:"metadata"`
    Spec struct {
        Replicas int `yaml:"replicas"`
        Template struct {
            Spec struct {
                Containers []struct {
                    Name  string `yaml:"name"`
                    Image string `yaml:"image"`
                } `yaml:"containers"`
            } `yaml:"spec"`
        } `yaml:"template"`
    } `yaml:"spec"`
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run k8s-reader.go <deployment.yaml>")
        os.Exit(1)
    }
    
    filename := os.Args[1]
    data, err := os.ReadFile(filename)
    if err != nil {
        fmt.Printf("Error reading file: %v\n", err)
        os.Exit(1)
    }
    
    var deployment Deployment
    if err := yaml.Unmarshal(data, &deployment); err != nil {
        fmt.Printf("Error parsing YAML: %v\n", err)
        os.Exit(1)
    }
    
    fmt.Println("=== Kubernetes Deployment Info ===")
    fmt.Printf("Name: %s\n", deployment.Metadata.Name)
    fmt.Printf("Namespace: %s\n", deployment.Metadata.Namespace)
    fmt.Printf("Replicas: %d\n", deployment.Spec.Replicas)
    fmt.Println("\nContainers:")
    for i, container := range deployment.Spec.Template.Spec.Containers {
        fmt.Printf("  %d. %s: %s\n", i+1, container.Name, container.Image)
    }
}
```

**Create `deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: default
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: nginx:latest
      - name: sidecar
        image: busybox:latest
```

**Run:**
```bash
go run k8s-reader.go deployment.yaml
```

---

### 17. Concurrent Tasks - Multi-Server Health Check

**Create `multi-healthcheck.go`:**
```go
package main

import (
    "fmt"
    "net/http"
    "sync"
    "time"
)

type ServerStatus struct {
    Name    string
    URL     string
    Status  string
    Latency time.Duration
    Error   error
}

func checkServer(name, url string, wg *sync.WaitGroup, results chan<- ServerStatus) {
    defer wg.Done()
    
    start := time.Now()
    client := http.Client{Timeout: 5 * time.Second}
    
    resp, err := client.Get(url)
    latency := time.Since(start)
    
    status := ServerStatus{
        Name:    name,
        URL:     url,
        Latency: latency,
        Error:   err,
    }
    
    if err != nil {
        status.Status = "DOWN"
    } else {
        defer resp.Body.Close()
        if resp.StatusCode >= 200 && resp.StatusCode < 300 {
            status.Status = "UP"
        } else {
            status.Status = "DEGRADED"
        }
    }
    
    results <- status
}

func main() {
    servers := []struct {
        name string
        url  string
    }{
        {"Google", "https://www.google.com"},
        {"GitHub", "https://www.github.com"},
        {"Docker Hub", "https://hub.docker.com"},
        {"Kubernetes", "https://kubernetes.io"},
    }
    
    var wg sync.WaitGroup
    results := make(chan ServerStatus, len(servers))
    
    // Start health checks concurrently
    for _, s := range servers {
        wg.Add(1)
        go checkServer(s.name, s.url, &wg, results)
    }
    
    // Close channel when all goroutines complete
    go func() {
        wg.Wait()
        close(results)
    }()
    
    // Collect results
    fmt.Println("=== Health Check Results ===\n")
    for status := range results {
        if status.Error != nil {
            fmt.Printf("❌ %s: %s (Error: %v)\n", status.Name, status.Status, status.Error)
        } else {
            fmt.Printf("✅ %s: %s (Latency: %v)\n", status.Name, status.Status, status.Latency)
        }
    }
    
    fmt.Println("\nAll checks complete!")
}
```

**Run:**
```bash
go run multi-healthcheck.go
```

---

### 18. File Watcher - Auto-Reload Config

**Create `filewatcher.go`:**
```go
package main

import (
    "fmt"
    "os"
    "time"
)

type Config struct {
    ReloadCount int
    LastReload  time.Time
}

var config = &Config{}

func loadConfig() {
    config.ReloadCount++
    config.LastReload = time.Now()
    fmt.Printf("[%s] Config reloaded (count: %d)\n", 
        config.LastReload.Format("15:04:05"), config.ReloadCount)
}

func watchFile(filename string) {
    var lastModTime time.Time
    
    // Get initial modification time
    if info, err := os.Stat(filename); err == nil {
        lastModTime = info.ModTime()
        fmt.Printf("Watching file: %s (initial load)\n", filename)
        loadConfig()
    }
    
    // Check for changes every second
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()
    
    for range ticker.C {
        info, err := os.Stat(filename)
        if err != nil {
            fmt.Printf("Error checking file: %v\n", err)
            continue
        }
        
        if info.ModTime().After(lastModTime) {
            lastModTime = info.ModTime()
            loadConfig()
        }
    }
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run filewatcher.go <config-file>")
        os.Exit(1)
    }
    
    filename := os.Args[1]
    
    fmt.Println("File watcher started. Modify the file to trigger reload.")
    fmt.Println("Press Ctrl+C to stop.\n")
    
    watchFile(filename)
}
```

**Create `config.txt`:**
```
# Configuration file
server_port=8080
debug=true
```

**Run:**
```bash
go run filewatcher.go config.txt

# In another terminal, modify config.txt to see reload
```

---

## Quick Reference

### Common Go Commands

```bash
# Run program
go run main.go

# Build executable
go build main.go

# Format code
go fmt ./...

# Install dependency
go get package-name

# Tidy dependencies
go mod tidy

# Run tests
go test ./...
```

### Useful Packages for DevOps

```go
// HTTP
import "net/http"

// File operations
import "os"
import "io/ioutil"

// JSON
import "encoding/json"

// YAML
import "gopkg.in/yaml.v3"

// Time
import "time"

// Command execution
import "os/exec"

// Logging
import "log"
```

---

## Next Steps

1. **Practice**: Run all examples and modify them
2. **Build Tools**: Create your own CLI tools
3. **Learn More**: 
   - Go standard library: https://pkg.go.dev/std
   - Go by Example: https://gobyexample.com
4. **DevOps Libraries**:
   - Kubernetes client: `k8s.io/client-go`
   - Docker client: `github.com/docker/docker/client`
   - Terraform: `github.com/hashicorp/terraform`

Happy coding with Go! 🚀

