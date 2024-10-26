# Plex-programming-language
## WARNING: This compiler is full of bugs ! If you would like to contribute to this project, feel free to open a pull request. Most of the code provided in the documentation will not work. The code in [script.nvs](script.nvs)

---
# **NovaScript Language Documentation**

## **1. Program Structure**

Every NovaScript program starts with `PROGRAM BEGIN` and ends with `PROGRAM END`. Optional descriptive information can be added at the beginning for readability.

```nova
PROGRAM BEGIN
    DESCRIPTION "Example program"
    AUTHOR "Plexi09"
    DATE "2024-10-26"
    
    # Code goes here
PROGRAM END
```

## **2. Variable Declaration**

NovaScript supports `num` (number), `str` (string), `bool` (boolean), and `list`. Variables can be statically or dynamically typed.

```nova
num x = 10
str message = "Hello"
bool isActive = true
y = 3.14  # Dynamic typing
```

## **3. Functions**

Functions are defined with `func`, and `end` signifies the end of the function. Parameters and return types are optional but recommended for clarity.

```nova
func greet(name: str) return str
    return "Hello, " + name + "!"
end
```

### **Function Call**

```nova
str result = greet("Alice")
```

## **4. Control Structures**

### **4.1 Conditions**

Conditions use `if`, `then`, `else if`, and `else`, with `end` to mark the block’s conclusion.

```nova
if age >= 18 then
    display "Adult"
else if age >= 13 then
    display "Teenager"
else
    display "Child"
end
```

### **4.2 Loops**

NovaScript includes `for` and `while` loops, ending with `end`.

#### **For Loop**

```nova
list numbers = [1, 2, 3, 4, 5]
for num in numbers do
    display i
end
```

#### **While Loop**

```nova
num count = 0
while count < 5 do
    display count
    count += 1
end
```

## **5. Error Handling**

Use `try`, `except`, and `end` for exception handling.

```nova
func divide(a: num, b: num) return num
    try
        return a / b
    except Exception
        display "Error: Division by zero"
        display "Exception: " + Exception
        return 0
    end
end
```

## **6. Modules and Importing**

Use `use` to import modules for built-in functions like string and math operations. You can also import external libraries by putting them in the `lib` folder of your current project.

```nova
use strlib
use mathlib

strlib.upper("hello")  # Converts to "HELLO"
mathlib.sqrt(16)       # Returns 4.0
```

## **7. Displaying Output**

Use `display` to print values to the console.

```nova
display "Hello, World!"
display x  # Prints the value of x
```

## **8. Comments**

- **Single-line comments:** Begin with `#`
- **Multi-line comments:** Use `/* ... */`

```nova
# This is a single-line comment
/*
This is a
multi-line comment
*/
```

## **9. Additional Features**

### **9.1 Type Inference**

NovaScript supports type inference, allowing variables to be declared without an explicit type when initializing.

```nova
z = "This is a string"  # Type inferred as str
y = [1, 2, 3, 4, 5] # Type ubferred as list
```

### **9.2 List Manipulation**

You can manipulate lists using built-in functions for common operations.

```nova
list items = [1, 2, 3]
items.append(4)           # Adds 4 to the list
num length = items.length()  # Gets the length of the list
```

### **9.3 Object-Oriented Features**

NovaScript allows the creation of classes and objects, promoting object-oriented programming.

```nova
class Person
    str name
    num age

    func init(name: str, age: num)
        this.name = name
        this.age = age
    end

    func greet() return str
        return "Hello, my name is " + this.name + " and I am " + this.age + " years old."
    end
end

Person john = Person("John", 30)
display john.greet()
```

---
