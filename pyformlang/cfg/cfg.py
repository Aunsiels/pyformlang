""" A context free grammar """

from typing import AbstractSet, List, Iterable, Tuple, Dict, Any

from .variable import Variable
from .terminal import Terminal
from .production import Production
from .cfg_object import CFGObject
from .epsilon import Epsilon
from .utils import to_variable, to_terminal


class CFG(object):
    """ A class representing a context free grammar

    Parameters
    ----------
    variables : set of :class:`~pyformlang.cfg.Variable`, optional
        The variables of the CFG
    terminals : set of :class:`~pyformlang.cfg.Terminal`, optional
        The terminals of the CFG
    start_symbol : :class:`~pyformlang.cfg.Variable`, optional
        The start symbol
    productions : set of :class:`~pyformlang.cfg.Production`, optional
        The productions or rules of the CFG
    """

    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: AbstractSet[Production] = None):
        if variables is not None:
            variables = set([to_variable(x) for x in variables])
        self._variables = variables or set()
        self._variables = set(self._variables)
        if terminals is not None:
            terminals = set([to_terminal(x) for x in terminals])
        self._terminals = terminals or set()
        self._terminals = set(self._terminals)
        if start_symbol is not None:
            start_symbol = to_variable(start_symbol)
        self._start_symbol = start_symbol
        if start_symbol is not None:
            self._variables.add(start_symbol)
        self._productions = productions or set()
        self._productions = set(self._productions)
        for production in self._productions:
            self._variables.add(production.get_head())
            for cfg_object in production.get_body():
                if isinstance(cfg_object, Terminal):
                    if cfg_object != Epsilon():
                        self._terminals.add(cfg_object)
                else:
                    self._variables.add(cfg_object)
        self._normal_form = None

    def get_number_variables(self) -> int:
        """ Returns the number of Variables

        Returns
        ----------
        n_variables : int
            The number of variables
        """
        return len(self._variables)

    def get_number_terminals(self) -> int:
        """ Returns the number of Terminals

        Returns
        ----------
        n_terminals : int
            The number of terminals
        """
        return len(self._terminals)

    def get_number_productions(self) -> int:
        """ Returns the number of Productions

        Returns
        ----------
        n_productions : int
            The number of productions
        """
        return len(self._productions)

    def get_generating_symbols(self) -> AbstractSet[CFGObject]:
        """ Gives the objects which are generating in the CFG

        Returns
        ----------
        generating_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The generating symbols of the CFG
        """
        return self._get_generating_or_nullable(False)

    def _get_generating_or_nullable(self, nullable=False):
        """ Merge of nullable and generating """
        g_symbols = set()
        g_symbols.add(Epsilon())
        productions = list(self._productions)
        to_process = []
        to_process.append(Epsilon())
        if not nullable:
            for terminal in self._terminals:
                g_symbols.add(terminal)
                to_process.append(terminal)
        symb_to_prod = dict()
        prod_occured = []
        prod_required = []
        prod_head = []
        for i, production in enumerate(productions):
            for member in production.get_body():
                if member in symb_to_prod:
                    symb_to_prod[member].append(i)
                else:
                    symb_to_prod[member] = [i]
            prod_occured.append(0)
            prod_required.append(len(production.get_body()))
            prod_head.append(production.get_head())
            if prod_required[-1] == 0 and prod_head[-1] not in g_symbols:
                g_symbols.add(prod_head[-1])
                to_process.append(prod_head[-1])
        while to_process:
            current = to_process.pop()
            for i in symb_to_prod.get(current, []):
                prod_occured[i] += 1
                if prod_occured[i] == prod_required[i] and prod_head[i] not in g_symbols:
                    g_symbols.add(prod_head[i])
                    to_process.append(prod_head[i])
        g_symbols.remove(Epsilon())
        return g_symbols

    def get_reachable_symbols(self) -> AbstractSet[CFGObject]:
        """ Gives the objects which are reachable in the CFG

        Returns
        ----------
        reachable_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The reachable symbols of the CFG
        """
        r_symbols = set()
        r_symbols.add(self._start_symbol)
        productions = self._productions.copy()
        found_modification = True
        while found_modification:
            found_modification = False
            used_productions = []
            for production in productions:
                if production.get_head() in r_symbols:
                    found_modification = True
                    used_productions.append(production)
                    for symbol in production.get_body():
                        if symbol != Epsilon():
                            r_symbols.add(symbol)
            for production in used_productions:
                productions.remove(production)
        return r_symbols

    def remove_useless_symbols(self) -> "CFG":
        """ Removes useless symbols in a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG without useless symbols
        """
        generating = self.get_generating_symbols()
        productions = [x for x in self._productions
                       if x.get_head() in generating and
                       all([y in generating for y in x.get_body()])]
        new_var = self._variables.intersection(generating)
        new_ter = self._terminals.intersection(generating)
        cfg_temp = CFG(new_var, new_ter, self._start_symbol, productions)
        reachables = cfg_temp.get_reachable_symbols()
        productions = [x for x in productions
                       if x.get_head() in reachables]
        new_var = new_var.intersection(reachables)
        new_ter = new_ter.intersection(reachables)
        return CFG(new_var, new_ter, self._start_symbol, productions)

    def get_nullable_symbols(self) -> AbstractSet[CFGObject]:
        """ Gives the objects which are nullable in the CFG

        Returns
        ----------
        nullable_symbols : set of :class:`~pyformlang.cfg.CFGObject`
            The nullable symbols of the CFG
        """
        return self._get_generating_or_nullable(True)

    def remove_epsilon(self) -> "CFG":
        """ Removes the epsilon of a cfg

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG without epsilons
        """
        new_productions = []
        nullables = self.get_nullable_symbols()
        for production in self._productions:
            new_productions += remove_nullable_production(production, nullables)
        return CFG(self._variables,
                   self._terminals,
                   self._start_symbol,
                   set(new_productions))

    def get_unit_pairs(self) -> AbstractSet[Tuple[Variable, Variable]]:
        """ Finds all the unit pairs

        Returns
        ----------
        unit_pairs : set of tuple of :class:`~pyformlang.cfg.Variable`
            The unit pairs
        """
        unit_pairs = set()
        for variable in self._variables:
            unit_pairs.add((variable, variable))
        productions = [x for x in self._productions if len(x.get_body()) == 1 and\
                                                       isinstance(x.get_body()[0], Variable)]
        productions_d = get_productions_d(productions)
        to_process = list(unit_pairs)
        while to_process:
            var_A, var_B = to_process.pop()
            for production in productions_d.get(var_B, []):
                temp = (var_A, production.get_body()[0])
                if temp not in unit_pairs:
                    unit_pairs.add(temp)
                    to_process.append(temp)
        return unit_pairs

    def eliminate_unit_productions(self) -> "CFG":
        """ Eliminate all the unit production in the CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG equivalent without unit productions
        """
        unit_pairs = self.get_unit_pairs()
        productions = [x for x in self._productions if len(x.get_body()) != 1 or\
                                                       not isinstance(x.get_body()[0], Variable)]
        productions_d = get_productions_d(productions)
        new_productions = set()
        for var_A, var_B in unit_pairs:
            for production in productions_d.get(var_B, []):
                new_productions.add(Production(var_A,
                                               production.get_body()))
        return CFG(self._variables,
                   self._terminals,
                   self._start_symbol,
                   set(productions).union(new_productions))

    def _get_productions_with_only_single_terminals(self):
        """ Remove the terminals involved in a body of length more than 1 """
        term_to_var = dict()
        new_productions = []
        for terminal in self._terminals:
            var = Variable(str(terminal.get_value()) + "#CNF#")
            term_to_var[terminal] = var
        # We want to add only the useful productions
        used = set()
        for production in self._productions:
            if len(production.get_body()) == 1:
                new_productions.append(production)
                continue
            new_body = []
            for symbol in production.get_body():
                if symbol in term_to_var:
                    new_body.append(term_to_var[symbol])
                    used.add(symbol)
                else:
                    new_body.append(symbol)
            new_productions.append(Production(production.get_head(),
                                              new_body))
        for terminal in used:
            new_productions.append(Production(term_to_var[terminal], [terminal]))
        return new_productions

    def _get_next_free_variable(self, idx, prefix):
        idx += 1
        temp = Variable(prefix + str(idx))
        while temp in self._variables:
            idx += 1
            temp = Variable(prefix + str(idx))
        return idx, temp

    def _decompose_productions(self, productions):
        """ Decompose productions """
        idx = 0
        new_productions = []
        done = dict()
        for production in productions:
            body = production.get_body()
            if len(body) <= 2:
                new_productions.append(production)
                continue
            new_var = []
            for _ in range(len(body) - 2):
                idx, var = self._get_next_free_variable(idx, "C#CNF#")
                new_var.append(var)
            head = production.get_head()
            stopped = False
            for i in range(len(body) - 2):
                temp = tuple(body[i+1:])
                if temp in done:
                    new_productions.append(Production(head,
                                                      (body[i], done[temp])))
                    stopped = True
                    break
                new_productions.append(Production(head, (body[i], new_var[i])))
                done[temp] = new_var[i]
                head = new_var[i]
            if not stopped:
                new_productions.append(Production(head, [body[-2], body[-1]]))
        return new_productions

    def to_normal_form(self) -> "CFG":
        """ Gets the Chomsky Normal Form of a CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG equivalent in the CNF form
        """
        if self._normal_form is not None:
            return self._normal_form
        nullables = self.get_nullable_symbols()
        unit_pairs = self.get_unit_pairs()
        generating = self.get_generating_symbols()
        reachables = self.get_reachable_symbols()
        if len(nullables) != 0 or len(unit_pairs) != len(self._variables) or\
                len(generating) != len(self._variables) + len(self._terminals) or \
                len(reachables) != len(self._variables) + len(self._terminals):
            if len(self._productions) == 0:
                self._normal_form = self
                return self
            new_cfg = self.remove_epsilon()\
                          .eliminate_unit_productions()\
                          .remove_useless_symbols()
            cfg = new_cfg.to_normal_form()
            self._normal_form = cfg
            return cfg
        # Remove terminals from body
        new_productions = self._get_productions_with_only_single_terminals()
        new_productions = self._decompose_productions(new_productions)
        cfg = CFG(start_symbol=self._start_symbol,
                  productions=set(new_productions))
        self._normal_form = cfg
        return cfg

    def get_variables(self) -> AbstractSet[Variable]:
        """ Gives the variables

        Returns
        ----------
        variables : set of :class:`~pyformlang.cfg.Variable`
            The variables of the CFG
        """
        return self._variables.copy()

    def get_terminals(self) -> AbstractSet[Terminal]:
        """ Gives the terminals

        Returns
        ----------
        terminals : set of :class:`~pyformlang.cfg.Terminal`
            The terminals of the CFG
        """
        return self._terminals.copy()

    def get_productions(self) -> AbstractSet[Production]:
        """ Gives the productions

        Returns
        ----------
        productions : set of :class:`~pyformlang.cfg.Production`
            The productions of the CFG
        """
        return self._productions.copy()

    def get_start_symbol(self) -> Variable:
        """ Gives the start symbol

        Returns
        ----------
        start_variable : :class:`~pyformlang.cfg.Variable`
            The start symbol of the CFG
        """
        return self._start_symbol

    def substitute(self, substitution: Dict[Terminal, "CFG"]) -> "CFG":
        """ Subsitutes CFG to terminals in the current CFG

        Parameters
        -----------
        subsitution : dict of :class:`~pyformlang.cfg.Terminal` to :class:`~pyformlang.cfg.CFG`
            A substitution

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A new CFG recognizing the substitution
        """
        idx = 0
        suffix = "#SUBS#"
        new_variables_d = dict()
        new_vars = set()
        for variable in self._variables:
            temp = Variable(variable.get_value() + suffix + str(idx))
            new_variables_d[variable] = temp
            new_vars.add(temp)
            idx += 1
        productions = []
        terminals = self._terminals.copy()
        final_replacement = dict()
        for ter, cfg in substitution.items():
            new_variables_d_local = dict()
            for variable in cfg.get_variables():
                temp = Variable(variable.get_value() + suffix + str(idx))
                new_variables_d_local[variable] = temp
                new_vars.add(temp)
                idx += 1
            # Add rules of the new cfg
            for production in cfg.get_productions():
                body = []
                for cfgobj in production.get_body():
                    if cfgobj in new_variables_d_local:
                        body.append(new_variables_d_local[cfgobj])
                    else:
                        body.append(cfgobj)
                productions.append(Production(new_variables_d_local[production.get_head()],
                                              body))
            final_replacement[ter] = new_variables_d_local[cfg.get_start_symbol()]
            terminals = terminals.union(cfg.get_terminals())
        for production in self._productions:
            body = []
            for cfgobj in production.get_body():
                if cfgobj in new_variables_d:
                    body.append(new_variables_d[cfgobj])
                elif cfgobj in final_replacement:
                    body.append(final_replacement[cfgobj])
                else:
                    body.append(cfgobj)
            productions.append(Production(new_variables_d[production.get_head()],
                                          body))
        return CFG(new_vars, None, new_variables_d[self._start_symbol],
                   set(productions))

    def union(self, other: "CFG") -> "CFG":
        """ Makes the union of two CFGs

        Parameters
        ----------
        other : :class:`~pyformlang.cfg.CFG`
            The other CFG to unite with

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG resulting of the union of the two CFGs
        """
        start_temp = Variable("#STARTUNION#")
        temp_0 = Terminal("#0UNION#")
        temp_1 = Terminal("#1UNION#")
        p0 = Production(start_temp, [temp_0])
        p1 = Production(start_temp, [temp_1])
        cfg_temp = CFG({start_temp},
                       {temp_0, temp_1},
                       start_temp,
                       {p0, p1})
        return cfg_temp.substitute({temp_0: self,
                                    temp_1: other})

    def concatenate(self, other: "CFG") -> "CFG":
        """ Makes the concatenation of two CFGs

        Parameters
        ----------
        other : :class:`~pyformlang.cfg.CFG`
            The other CFG to concatenate with

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The CFG resulting of the concatenation of the two CFGs
        """
        start_temp = Variable("#STARTCONC#")
        temp_0 = Terminal("#0CONC#")
        temp_1 = Terminal("#1CONC#")
        p0 = Production(start_temp, [temp_0, temp_1])
        cfg_temp = CFG({start_temp},
                       {temp_0, temp_1},
                       start_temp,
                       {p0})
        return cfg_temp.substitute({temp_0: self,
                                    temp_1: other})

    def get_closure(self) -> "CFG":
        """ Gets the closure of the CFG (*)

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The closure of the current CFG
        """
        start_temp = Variable("#STARTCLOS#")
        temp_1 = Terminal("#1CLOS#")
        p0 = Production(start_temp, [temp_1])
        p1 = Production(start_temp, [start_temp, start_temp])
        p2 = Production(start_temp, [])
        cfg_temp = CFG({start_temp},
                       {temp_1},
                       start_temp,
                       {p0, p1, p2})
        return cfg_temp.substitute({temp_1: self})

    def get_positive_closure(self) -> "CFG":
        """ Gets the positive closure of the CFG (+)

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            The positive closure of the current CFG
        """
        start_temp = Variable("#STARTPOSCLOS#")
        var_temp = Variable("#VARPOSCLOS#")
        temp_1 = Terminal("#1POSCLOS#")
        p0 = Production(start_temp, [temp_1, var_temp])
        p1 = Production(var_temp, [var_temp, var_temp])
        p2 = Production(var_temp, [temp_1])
        p3 = Production(var_temp, [])
        cfg_temp = CFG({start_temp, var_temp},
                       {temp_1},
                       start_temp,
                       {p0, p1, p2, p3})
        return cfg_temp.substitute({temp_1: self})

    def reverse(self) -> "CFG":
        """ Reverse the current CFG

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            Reverse the current CFG
        """
        productions = []
        for production in self._productions:
            productions.append(Production(production.get_head(),
                                          production.get_body()[::-1]))
        return CFG(self.get_variables(),
                   self.get_terminals(),
                   self.get_start_symbol(),
                   productions)

    def is_empty(self) -> bool:
        """ Says whether the CFG is empty or not

        Returns
        ----------
        is_empty : bool
            Whether the CFG is empty or not

        TODO
        ----------
        Can be optimized
        """
        return self._start_symbol not in self.get_generating_symbols()

    def _generate_epsilon(self):
        """ Whether the grammar generates epsilon or not

        Returns
        ----------
        generate_epsilon : bool
            Whether epsilon is generated or not by the CFG
        """
        generate_epsilon = {Epsilon()}
        productions = self._productions.copy()
        found_modification = True
        while found_modification:
            found_modification = False
            used_productions = []
            for production in productions:
                if all([x in generate_epsilon for x in production.get_body()]):
                    if production.get_head() == self._start_symbol:
                        return True
                    generate_epsilon.add(production.get_head())
                    found_modification = True
                    used_productions.append(production)
            for production in used_productions:
                productions.remove(production)
        return False

    def contains(self, word: Iterable[Terminal]) -> bool:
        """ Gives the membership of a word to the grammar

        Parameters
        ----------
        word : iterable of :class:`~pyformlang.cfg.CFG`
            The word to check

        Returns
        ----------
        contains : bool
            Whether word if in the CFG or not
        """
        # Remove epsilons
        word = [to_terminal(x) for x in word if x != Epsilon()]
        if not word:
            return self._generate_epsilon()
        cnf = self.to_normal_form()
        cyk_table = dict()
        # Organize productions
        productions_d = dict()
        for production in cnf.get_productions():
            temp = tuple(production.get_body())
            if temp in productions_d:
                productions_d[temp].append(production.get_head())
            else:
                productions_d[temp] = [production.get_head()]
        # Initialization
        for i, ai in enumerate(word):
            if (ai,) in productions_d:
                cyk_table[(i, i+1)] = set(productions_d[(ai,)])
            else:
                return False
        for j in range(2, len(word) + 1):
            for i in range(len(word) - j + 1):
                cyk_table[(i, i + j)] = set()
                for k in range(i + 1, i + j):
                    for B in cyk_table.setdefault((i, k), set()):
                        for C in cyk_table.setdefault((k, i + j), set()):
                            for A in productions_d.setdefault((B, C), []):
                                cyk_table[(i, i + j)].add(A)
        return cnf.get_start_symbol() in cyk_table[(0, len(word))]

    def to_pda(self) -> "pda.PDA":
        """ Convert the CFG to a PDA equivalent on empty stack

        Returns
        ----------
        new_pda : :class:`~pyformlang.pda.PDA`
            The equivalent PDA
        """
        from pyformlang import pda
        state = pda.State("q")
        input_symbols = [to_pda_object(x, pda.Symbol) for x in self._terminals]
        stack_alphabet = [to_pda_object(x, pda.StackSymbol)
                          for x in self._terminals.union(self._variables)]
        start_stack_symbol = to_pda_object(self._start_symbol, pda.StackSymbol)
        new_pda = pda.PDA(states={state},
                          input_symbols=input_symbols,
                          stack_alphabet=stack_alphabet,
                          start_state=state,
                          start_stack_symbol=start_stack_symbol)
        for production in self._productions:
            new_pda.add_transition(state, pda.Epsilon(),
                                   to_pda_object(production.get_head(),
                                                 pda.StackSymbol),
                                   state,
                                   [to_pda_object(x, pda.StackSymbol)
                                    for x in production.get_body()])
        for terminal in self._terminals:
            new_pda.add_transition(state, to_pda_object(terminal, pda.Symbol),
                                   to_pda_object(terminal, pda.StackSymbol),
                                   state, [])
        return new_pda

    def intersection(self, other: Any) -> "CFG":
        """ Gives the intersection of the current CFG with an other object

        Parameters
        ----------
        other : any
            The other object

        Returns
        ----------
        new_cfg : :class:`~pyformlang.cfg.CFG`
            A CFG representing the intersection with the other object

        Raises
        ----------
        TODO
        """
        pda = self.to_pda().to_final_state()
        pda_i = pda.intersection(other)
        return pda_i.to_empty_stack().to_cfg()

    def get_words(self, max_length: int=-1):
        """ Get the words generated by the CFG

        Parameters
        ----------
        max_length : int
            The maximum length of the words to return
        """
        nullables = self.get_nullable_symbols()
        if self.get_start_symbol() in nullables:
            yield []
        if max_length == 0:
            return
        cfg = self.to_normal_form()
        productions = cfg.get_productions()
        gen_d = dict()
        # Look for Epsilon Transitions
        for production in productions:
            if production.get_head() not in gen_d:
                gen_d[production.get_head()] = [[]]
            if len(production.get_body()) == 2:
                for obj in production.get_body():
                    if obj not in gen_d:
                        gen_d[obj] = [[]]
        # To a single terminal
        for production in productions:
            body = production.get_body()
            if len(body) == 1:
                if len(gen_d[production.get_head()]) == 1:
                    gen_d[production.get_head()].append([])
                if body not in gen_d[production.get_head()][-1]:
                    gen_d[production.get_head()][-1].append(list(body))
                    if production.get_head() == cfg.get_start_symbol():
                        yield list(body)
        # Complete what is missing
        current_length = 2
        total_no_modification = 0
        while current_length <= max_length or max_length == -1:
            was_modified = False
            for key in gen_d:
                if len(gen_d[key]) != current_length:
                    gen_d[key].append([])
            for production in productions:
                body = production.get_body()
                if len(gen_d[production.get_head()]) != current_length + 1:
                    gen_d[production.get_head()].append([])
                if len(body) != 2:
                    continue
                for i in range(1, current_length):
                    j = current_length - i
                    for left in gen_d[body[0]][i]:
                        for right in gen_d[body[1]][j]:
                            new_word = left + right
                            if new_word not in gen_d[production.get_head()][-1]:
                                was_modified = True
                                gen_d[production.get_head()][-1].append(new_word)
                                if production.get_head() == cfg.get_start_symbol():
                                    yield new_word
            if was_modified:
                total_no_modification = 0
            else:
                total_no_modification += 1
            current_length += 1
            if total_no_modification > current_length / 2:
                return


def to_pda_object(cfgobject: CFGObject, to_type) -> "pda.Symbol":
    """ Turns the object to a PDA symbol """
    from pyformlang import pda
    if isinstance(cfgobject, Epsilon):
        return pda.Epsilon()
    elif isinstance(cfgobject, Terminal):
        if to_type == pda.Symbol:
            return to_type(cfgobject.get_value())
        return to_type("#Term#" + str(cfgobject.get_value()))
    elif isinstance(cfgobject, Variable):
        return to_type("#Var#" + str(cfgobject.get_value()))
def remove_nullable_production_sub(body: Iterable[CFGObject],
                                   nullables: AbstractSet[CFGObject]) -> List[List[CFGObject]]:
    """ Recursive sub function to remove nullable objects """
    if not body:
        return [[]]
    all_next = remove_nullable_production_sub(body[1:], nullables)
    res = []
    for body_temp in all_next:
        if body[0] in nullables:
            res.append(body_temp)
        if body[0] != Epsilon():
            res.append([body[0]] + body_temp.copy())
    return res

def remove_nullable_production(production: Production,
                               nullables: AbstractSet[CFGObject]) -> List[Production]:
    """ Get all combinations of productions rules after removing nullable """
    next_prod_l = remove_nullable_production_sub(production.get_body(),
                                               nullables)
    res = []
    for prod_l in next_prod_l:
        if prod_l:
            res.append(Production(production.get_head(),
                                  prod_l))
    return res

def get_productions_d(productions):
    """ Get productions as a dictionary """
    productions_d = dict()
    for production in productions:
        l = productions_d.setdefault(production.get_head(), [])
        l.append(production)
    return productions_d
