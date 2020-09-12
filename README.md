# Rudito
This is a turing-complete programming language which needs different approach to code.

## Concept
This language has Three components
* Head 
* Execution
* Tail

### Head
Head component is like a checkpoint in code so that code execution will be redirected to this point whenever need.<br/>
It is represented by "/ /" delimiter.
### Execution
Execution is the main component where checking conditions and executing function happens.<br/>
It is represented by [ ( ) ].<br/>
[function1(condition)function2] is the syntax for this component.<br/>
Here function1 is executed if condition returns true else it executes function2.<br/>
If a function needs to be executed without checking any condition "()" is not required.<br/>
### Tail
Tail is the component which decides location of next code.<br/>
It is represented by "| |" delimter.<br/>
The name of Head component needs to be given inside the delimeter.<br/>
By default compiler goes to next line if Tail component is missing.<br/> 

## Data Types Supported
* Integer
* Boolean
* Float
* String

## Examples
