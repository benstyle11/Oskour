# Custom Constraints

## Why custom constraints ?

People at this event sometimes don't like each other, or like each other, or *reaaally* want to play with someone else. Hence, some customizable constraints are necessary.

N.B: These are the reasons why people thought this problem to be not automatizable.

## How ?
In order to create a custom constraint, create in your input folder a file named ```custom_constraint.yaml```. This file will contain all the custom constraints of the problem. As a yaml file, it should be written as follows:

1. Write every new constraint with a "-" at the beginning followed by the type of constraint:
```
- type: CopainsPjsScenarRonde
  [rest of the constraint]
  ...
- type: PasCopainsPjs
  [...]
- ...
```
- A constraint can be of the following types:


| Name | Effect | attributes |
| --------|--------|--------|
|CopainsPjsRonde |`equipe1` and `equip2` play together at `ronde` |`equipe1, equipe2, ronde` |
|CopainsPjMjScenar |`equipe1` plays `scenar` with `mj` at `ronde` | `equipe1, scenar, mj` |
|CopainsPjs |When both available, `equipe1` plays with `equipe2` (possibly multiple times) | `equipe1, equipe2` |
|PasCopainsPjs |`equipe1` **never** plays with `equipe2` |`equipe1, equipe2` |
|PjsScenarRonde | `equipe1` plays `scenar` at `ronde`  |`equipe1, scenar, ronde` |
|CopainsPjsScenarRonde |`equipe1` plays with `equipe2` `scenar` at `ronde` |`equipe1, equipe2, scenar, ronde` |

It should be noted that these are not "independant", i.e. CopainsPjsRonde combined with PjsScenarRonde is equivalent to CopainsPjsScenarRonde.

2. After the ```- type: [...]``` attributes, other attributes are to be added after (note that order is **not** important), e.g.:

``` 
- type:CopainsPjs
  equipe1: Jean Baptiste
  equipe2: Jean Eude
```

A missing attribute will yield a ```KeyError``` with the name of missing attribute.

**Every attribute is lower case, case should be respected for Ronde and equipe names.**

3. In principle, if the file is named correctly and placed in the input folder, `oskour` loads it automatically.

## But why do it in a text editor ?
In the future, a GUI may be written and allow for a more streamline experience, but for now you have to write the file as a yaml and no helper program is available.