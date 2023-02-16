import re
from DFG import remove_comments_and_docstrings
from tree_sitter import Language, Parser


BIN_OP = ['+', '-', '*', '/', '%', '&', '|', '^', '~', '!', '=', '>', '<', '?', ':', ',', '.',
          '==', '!=', '>', '<', '>=', '<=', '&&', '||', '++', '--', '<<', '>>', '>>>', '+=', '-=']


def calc_syntax_match(references, candidate, lang):
    return corpus_syntax_match([references], [candidate], lang)


def get_all_sub_trees(root_node, source_code):
    node_stack = []
    sub_tree_sexp_list = []
    depth = 1
    node_stack.append([root_node, depth])
    while len(node_stack) != 0:
        cur_node, cur_depth = node_stack.pop()

        sub_tree_sexp_list.append([cur_node.sexp(), cur_depth])

        for child_node in cur_node.children:
            if len(child_node.children) != 0 or child_node.type in BIN_OP:
                depth = cur_depth + 1
                node_stack.append([child_node, depth])
            else:
                print(child_node)

    return sub_tree_sexp_list


def corpus_syntax_match(references, candidates, lang):
    JAVA_LANGUAGE = Language('data/java-library.so', lang)
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    match_count = 0
    total_count = 0

    for i in range(len(candidates)):
        references_sample = references[i]
        candidate = candidates[i]
        for reference in references_sample:

            candidate = remove_comments_and_docstrings(candidate, 'java')
            reference = remove_comments_and_docstrings(reference, 'java')

            candidate_tree = parser.parse(bytes(candidate, 'utf8')).root_node
            reference_tree = parser.parse(bytes(reference, 'utf8')).root_node

            cand_sexps = [x[0]
                          for x in get_all_sub_trees(candidate_tree, candidate)]
            ref_sexps = get_all_sub_trees(reference_tree, reference)

            for sub_tree, depth in ref_sexps:
                if sub_tree in cand_sexps:
                    match_count += 1
            total_count += len(ref_sexps)

    score = match_count / total_count
    return score
