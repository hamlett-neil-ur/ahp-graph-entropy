# Evidentiary reasoning with the Analytic Hierarchy Process: Use of graph entropy to rank decision factors

## Abstract.

Decision makers often require insight into the relative strength of evidence influencing their choices. The Analytic Hierarchy Process (AHP) contains innate mechanisms leading to the rigorous quantification of decision factors' relative evidentiary strength. Pairwise-comparison analysis specifies edges for a complete, directed, acyclic graph, often called a *tournament graph*. Pairwise-comparison “preference ratios” provide tournament-graph edge weights, leading to a novel Laplacian matrix. Relative-entropy calculations based on Laplacians for induced subgraphs quantify the relative evidentiary strength associated with the decisional evidence ommitted from them. Relative-entropy *chain rules* provide mechanisms to couple hierarchically adjacent AHP tournament graphs into an overarching entropy structure for a multi-level decision problem.


## Draft research paper. 📝 

[`260504-ahp-graph-entropy.pdf`](./research-paper/260504-ahp-graph-entropy.pdf).

## 𝓣𝓸 𝓓𝓸. 🏗️🧱👷

### Couple the *sub-trees* of multi-level AHP formulation.

The sketched-out approach thus far considers only a two-tier sub-tree of a larger AHP problem. Its scope strictly spans the tournament graph defined by the pairwise comparisons. This at best provides only information of academic interest, or for trivial contexts. More-pragmatic applications, exempliefied by our case study [Bu, *et al* (2026)](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-materials/multi-criterion-decision-making/2605%20energy%20confersion%20and%20mgmt%20—%20multi-crieterion%20evaluation%20of%20symmetric%20tesli-like⋯.pdf), span multiple AHP sub-trees each defined by its own pairwise-comparison tournament graph.

***Lines of inquiry***.

* Can the AHP *priority vectors* be used for entropy-based coupling between tournament graphs for hierarchically-adjacent sub-trees? After all, we define priority vectors as unit-simplex projections. If we also think if them as probability distributions, can they provide an entropy mechanism by which to couple tournament graphs associated with subordinate sub-trees to the sub-tree of interest?

* 🌟 Entropy *chain rules*. Each pariwise-comparison edge list leads to an entropy structure associated with an AHP decision subtree. [Cover & Thomas (2026), §2.5](https://doi.org/10.1002/047174882X) presents chain rules for entropy, relative entropy, and mutual information. This provides rigorous coupling between the tournament graph for a given AHP decisional layer and that associated with its immediate constituent tournament graph. 🌟



# GitHub mechanics 🔧🔩🪛

## 1. Commit management.

### a. Visualize commit graph.

```bash
git log --oneline --graph
```


### b. Number of commits to a branch.

```bash
git rev-list --count <branch-main>
```

### c. Interactive rebase.

#### ⅰ. Identify the Starting Point.

To consolidate all 21 commits into a single cohesive commit, you need to reference the parent of the first commit in that sequence. The `-i` flag specified an interactive rebase.

```bash
git rebase -i --root 
```

#### ⅱ. The Interactive Todo List.

Your default text editor will open a list of your 21 commits, ordered from oldest (top) to newest (bottom). It will look something like this:

```text
pick a1b2c3d Commit message 1
pick e5f6g7h Commit message 2
pick i9j0k1l Commit message 3
  ⋮
pick m2n3o4p Commit message 21
```

#### ⅲ. Squash the Commits.
To consolidate, keep the first commit as pick and change all subsequent commits to `squash` (or just `s`).

pick: Use the commit.

squash: Use the commit, but meld it into the previous commit.

```text
pick a1b2c3d Commit message 1
squash e5f6g7h Commit message 2
squash i9j0k1l Commit message 3
   ⋮
squash m2n3o4p Commit message 21
```

#### ⅳ. Finalize the Commit Message.
Git will then open a second editor window showing all 21 original commit messages.

Delete the existing messages.

Write a new, clean summary of the combined work (e.g., "Implement evidentiary reasoning logic and graph entropy calculations").

Save and close.



### d. Consolidating commits to a branch (hard quash).

```bash
get fetch origin
git reset --soft $(git rev-list --max-parents=0 HEAD)
git commit --amend -m "Consolidated commit message"
git push --force-with-lease
```
