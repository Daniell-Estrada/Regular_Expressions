from models.tree import Tree
from models.afd import AFD
from utilities.infix_postfix import InfixPostFix
from utilities.symbol import Symbol


def main():
    regex = "cd(a|b)*xz"
    concat = Symbol('.')
    end_symbol = Symbol('$')

    ipt = InfixPostFix(regex)
    stack = ipt.convert()
    stack.append(end_symbol)
    stack.append(concat)
    aphabet = ipt.stack

    print('*** DFA Direct construction ***')
    print('\nAugmented postfix: ')
    for i in stack:
        print(i, end='')

    print('\nAlphabet: ')
    tree = Tree(stack)
    tree.show_tree(tree.root)
    afd = AFD(aphabet, tree)
    print(afd)




if __name__ == "__main__":
    main()
