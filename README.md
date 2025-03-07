## What This Is For

- This is a repository that contains a collection of rules that can be used with Midas
- Midas is a SAST tool that can be used to find security vulnerabilities and audit source code in line with organizational needs
- The rules in this repository follow the Midas rule format and have this spec

```yaml
rule_id: "test_rule"
rule_type: "Regex"
rule: "test_regex"
author: "test_author"
description: "test_description"
```

```yaml
rule_id: "test_rule"
rule_type: "Query"
rule: "MQL query"
author: "test_author"
description: "test_description"
```

The above rules show two use cases, one uses regular expressions for smaller pattern matching cases, while the other uses MQL queries for more complex vulnerabilities where you need a more expressive language.

MQL is currently under development, so the ruleset will not be complete/released until v0.1.0-Alpha is released for UAT. 

## How To Use This
```bash 
    midas -p ./src -r ./ruleset
    midas -p ./src -r ./ruleset -o ./output
    midas -p ./src -r default-c -o ./output
```

Midas can be used with local rulesets or with the default ruleset in v0.1.0-Alpha. Default will automatically pull all of the rules from this repository.

The appropriate way to use a default ruleset for a specific language is by specifying the short name of the language after default like so. 
- default-c
- default-cpp
- default-java
- default-py
- etc...

## Contributing
- Read the CONTRIBUTING.md documentation
- Make sure to follow the ruleset format and all tests pass prior to submitting a PR. Specifically the linter should pass and an associated code snippet should be found for the rule to display what the rule will trigger on.

## Rulesets
- The rulesets are organized by language and then type of rule. For example:

```
c/
├── lints/
│   ├── snippets/
│   │   ├── long_function.c
│   │   └── todo_lint.c
│   ├── long_function.yaml
│   └── todo_lint.yaml
    
cpp/
├── lints/
│   ├── snippets/
│   │   ├── long_function.cpp
│   │   ├── todo_lint.cpp
│   │   └── smart_pointer.cpp
│   ├── long_function.yaml
│   ├── todo_lint.yaml
│   └── smart_pointer.yaml
└── vulns/
    ├── snippets/
    │   ├── buffer_overflow.cpp
    │   └── integer_overflow.cpp
    ├── buffer_overflow.yaml
    └── integer_overflow.yaml
```

The above will be apparent from the initial structure from the base ruleset.

Feel free to develop your own rules for your use case locally, my only ask is if you find that rule useful to everybody else in general, feel free to submit a PR. Otherwise, this is yours to play with!

