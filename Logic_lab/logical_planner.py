from collections import deque

class Action:
    def __init__(self, name, pos_preconditions, neg_preconditions, pos_effects, neg_effects):
        self.name = name
        self.pos_preconditions = frozenset(pos_preconditions)
        self.neg_preconditions = frozenset(neg_preconditions)
        self.pos_effects = frozenset(pos_effects)
        self.neg_effects = frozenset(neg_effects)

    def is_applicable(self, state):
        return self.pos_preconditions <= state and self.neg_preconditions.isdisjoint(state)

    def apply(self, state):
        new_state = (state - self.neg_effects) | self.pos_effects
        return new_state

    def __repr__(self):
        return self.name

def bfs_plan(initial_state, actions, goal):
    initial_state = frozenset(initial_state)
    goal = frozenset(goal)
    if goal <= initial_state:
        return [], [initial_state]
    frontier = deque()
    frontier.append((initial_state, [], [initial_state]))
    visited = {initial_state}
    while frontier:
        state, plan, trace = frontier.popleft()
        for action in actions:
            if action.is_applicable(state):
                new_state = action.apply(state)
                if new_state in visited:
                    continue
                new_plan = plan + [action]
                new_trace = trace + [new_state]
                if goal <= new_state:
                    return new_plan, new_trace
                visited.add(new_state)
                frontier.append((new_state, new_plan, new_trace))
    return None, None

def run_planner(initial_state, actions, goal, label=""):
    print(f"\n=== {label} ===")
    print("Initial state:", set(initial_state))
    print("Goal:", set(goal))
    plan, trace = bfs_plan(initial_state, actions, goal)
    if plan is None:
        print("No plan found")
        return None
    print("Plan found:")
    for i, action in enumerate(plan, start=1):
        print(f"  {i}. {action.name}")
    print("States:")
    print(f"  S0: {set(trace[0])}")
    for i, (action, state) in enumerate(zip(plan, trace[1:]), start=1):
        print(f"  S{i} (after {action.name}): {set(state)}")
    return plan

def make_warehouse_actions(include_pickup=True, include_irrelevant_move=False):
    actions = []
    connections = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]
    for x, y in connections:
        actions.append(Action(
            name=f"Move(Robot,{x}->{y})",
            pos_preconditions={f"At(Robot,{x})"},
            neg_preconditions=set(),
            pos_effects={f"At(Robot,{y})"},
            neg_effects={f"At(Robot,{x})"}
        ))
    if include_pickup:
        for loc in ["A", "B", "C"]:
            actions.append(Action(
                name=f"PickUp(Package,{loc})",
                pos_preconditions={f"At(Robot,{loc})", f"At(Package,{loc})"},
                neg_preconditions=set(),
                pos_effects={"Holding(Package)"},
                neg_effects={f"At(Package,{loc})"}
            ))
    for loc in ["A", "B", "C"]:
        actions.append(Action(
            name=f"Drop(Package,{loc})",
            pos_preconditions={f"At(Robot,{loc})", "Holding(Package)"},
            neg_preconditions=set(),
            pos_effects={f"At(Package,{loc})"},
            neg_effects={"Holding(Package)"}
        ))
    if include_irrelevant_move:
        actions.append(Action(
            name="Move(Robot,A->C,direct-shortcut)",
            pos_preconditions={"At(Robot,A)"},
            neg_preconditions=set(),
            pos_effects={"At(Robot,C)"},
            neg_effects={"At(Robot,A)"}
        ))
    return actions

if __name__ == "__main__":
    initial_state = {"At(Robot,A)", "At(Package,A)"}
    goal = {"At(Package,C)"}
    actions_A = make_warehouse_actions(include_pickup=True)
    run_planner(initial_state, actions_A, goal, label="Test A: Solvable Problem")
    actions_B = make_warehouse_actions(include_pickup=False)
    run_planner(initial_state, actions_B, goal, label="Test B: Impossible Problem")
    actions_C = make_warehouse_actions(include_pickup=True, include_irrelevant_move=True)
    run_planner(initial_state, actions_C, goal, label="Test C: Irrelevant Actions")
