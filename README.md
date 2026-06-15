# Evidentiary reasoning with the Analytic Hierarchy Process: Use of graph entropy to rank decision factors

## Abstract.

 Decision makers often require insight into the relative strength of the elements of evidence on which their choices hinge. The Analytic Hierarchy Process (AHP) contains innate mechanisms leading to the rigorous quantification of elements' relative strength. Comparative judgements (“pairwise comparisons”) between elements of a given hierarchy model produce lists of edges for a complete graph. Under certain conditions, such graphs are also directed and acyclic, belonging to the class of tournament graphs. Intensities of Importance from comparative judgements provide weights for graphs' edges. Relative-entropy calculations based on Laplacian matrices for induced subgraphs quantify the relative evidentiary strength associated with the decisional evidence ommitted from them. Motivated by quantum-computing research, recent innovations in matrix representations of graphs support the idiosyncratic structures arising from comparative judgements. A previously published case study related to an offshore-pipeline material selection demonstrates the approach ([`Zheng, et al` (2005)](https://doi.org/10.1016/j.ijpvp.2025.105461)). The graph-entropy method provides greater strength-of-contribution contrast than sensitivity analysis from the case study.


## Draft research paper. 📝 

[`260528-ahp-graph-entropy.pdf`](https://drive.google.com/file/d/1BR45AW378_d-EXYlBj00NM6JgoaBYdBb).

## 𝓣𝓸 𝓓𝓸. 🏗️🧱👷

### Couple the *sub-trees* of multi-level AHP formulation.

The sketched-out approach thus far considers only a two-tier sub-tree of a larger AHP problem. Its scope strictly spans the tournament graph defined by the pairwise comparisons. This at best provides only information of academic interest, or for trivial contexts. More-pragmatic applications, exempliefied by our case study [`Zheng, et al (2026)`](https://doi.org/10.1016/j.ijpvp.2025.105461), span multiple AHP sub-trees each defined by its own pairwise-comparison tournament graph.

***Lines of inquiry***.

#### Coupling entropies of hierarchically adjacent hierarchy models.

🌟 Entropy *chain rules*. Each pariwise-comparison edge list leads to an entropy structure associated with an AHP decision subtree. [`Cover & Thomas (2026), §2.5`](https://doi.org/10.1002/047174882X) presents chain rules for entropy, relative entropy, and mutual information. This provides rigorous coupling between the tournament graph for a given AHP decisional layer and that associated with its immediate constituent tournament graph. 🌟

#### Graphical connection of hierarchically-adjacent comparative-judgement graphs.

Hierarchy-model tree graphs provide the *connective tissue*. Proiority-vector weights — unit-simplex projections — behave like probability distributions. [`Brown, et al (2020`](https://doi.org/10.1016/j.laa.2019.09.026) explore graph entropies based on spectra of normalized Laplacian matrices. 


### Weave in the [*Decision-Quality* (DQ)](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119176657) narrative more-deeply. 
Its appearance amplifies the theme of evidentiary reasoning. Given the current composition risks its appearance as tangential, gratuitious. If DQ becomes a more-central theme, then this work's attractiveness for certain target journals might be enhanced. Moreover, DQ must be differentiated from AHP. Naïve application of AHP mechanics can introduce logical contradictions — recently described, *e.g.*, by [`Abbas (2026)`](https://www.decisionprofessionals.com/events/simple-registration?CalendarEventKey=bd2fb3d0-7aa0-4d4e-a38d-019d891f176e&Home=%2fsdp-participate%2fevents). This stands in antithesis to the *Sound Reasoning* link in the DQ framework.


### Amplify the evidentiary-reasoning aspects of AHP.

As of commit [`735d77f96fd192ecdce3a2ecd11c35cd05bf49b4`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/tree/735d77f96fd192ecdce3a2ecd11c35cd05bf49b4), the case study focuses on the mechanics of AHP. Given the title and objective, some mention of the epistemology of AHP seems called-for. Spefically, AHP focuses on prioritization and ordering, in contrast with utility-optimization of mainstream decision theory. 

### Clarify AHP terminology.

Seminal work describing AHP — [`Saaty (1986)`](https://doi.org/10.1287/mnsc.32.7.841), [`Saaty (1994)`](https://doi.org/10.1287/inte.24.6.19), [`Saaty (2003)`](https://doi.org/10.1016/S0377-2217(02)00227-8) — suffer from terminological inconsistencies, imprecisions. For example, ambiguity accompanies use of the terms *criterion* and *element* associated with vertices in tree-graph representations of hierarchy models. Use of AHP in-general (see below) introduces potential tenuity in proposing this work for publication in some target peer-reviewed journals.  Tightening up the vernacular reinforces the logical coherence strived-for herein.

### Incorporate preemptive responses to axiomatic weakness in AHP.

#### Problem.

AHP suffers from axiomatic deficiencies, which result in logical contradictions. Rank-reversal arises as a commonly described example. Concomitantly, AHP — as defined by [Saaty (1986)](https://doi.org/10.1287/mnsc.32.7.841) — despite *axiomatic bravado* — violates the von Neumann/Morgensern Axioms (e.g., [Kochenderfer (2015), §3.1.1](https://doi.org/10.7551/mitpress/10187.001.0001)). This introduces pronounced risk that the work would not pass peer review en route to publication.

That [Saaty (1986)](https://doi.org/10.1287/mnsc.32.7.841) based judgement comparison on an arbitrary, ad hoc set of *intensities of importance* that receive widespread, unquestioning use — including by the selected case study [Bu, *et al* (2020)](https://doi.org/10.1016/j.laa.2019.09.026) — represents particular weakness.

#### Approach to resolution.

A cursory, 🤖AI🤖-assisted search produced three Google-Doc artifacts.

* ["Three strategies"](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/I%20am%20writing%20a%20formal%20paper%20that%20I%20would%20like%20to....gdoc);
* ["Specific litarature"](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/1.%20I%20see%20Lootsma%20and%20Barzilia%20at%20https%3A%20%20doi.org%20....gdoc); and
* ["von Neumann/Morgenstern axioms"](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/von%20neumann%20morgenstern%20axioms.gdoc). 

The `"Three strategies"` includes the recommendaiton for an information-theoretic emphasis. Prominently,
```text
       We treat the hierarchical decomposition not as an explicit expected utility 
       mapping under vNM assumptions, but rather as an informational network topology. 
       The derived principal eigenvectors represent steady-state probability distributions 
       over a unit simplex, isolating the structural configurations of decision criteria. 
       By assessing the graph entropy of these matrices, we measure the propagation of 
       evidentiary consistency rather than behavioral preference utility.
```

Congruent ideas already form the basis for the work's foundational logic. Alternatives to [Saaty's (1986)](https://doi.org/10.1287/mnsc.32.7.841) ad hoc intensity-of-importance scale already receive passing mention. These include personal probabilities ([Savage (1972)](https://store.doverpublications.com/products/9780486137100); [de Finetti (1974)](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119286387)), as well as more-empirical measurments along the lines of [Hubbard & Seiersen (2023)](https://doi.org/10.1002/9781119892335).

#### Plan of action.

* Cursorily address — pre [`arχiv.org`](https://arxiv.org/) posting — narratives appearing in the [`"Three strategies"`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/I%20am%20writing%20a%20formal%20paper%20that%20I%20would%20like%20to....gdoc) analysis.
* Work the more-robust recommendations from [`"Three strategies"`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/I%20am%20writing%20a%20formal%20paper%20that%20I%20would%20like%20to....gdoc) and [`"Specific litarature"`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/1.%20I%20see%20Lootsma%20and%20Barzilia%20at%20https%3A%20%20doi.org%20....gdoc) into the "Entropy of edge-weighted ⋯" section of the [`research paper`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/260504-ahp-graph-entropy.pdf). 
* Post a draft of [`research paper`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/260504-ahp-graph-entropy.pdf) to [`arχiv.org`](https://arxiv.org/).
* Weave into a subsequent revision — post [`arχiv.org`](https://arxiv.org/) posting — narratives appearing in the ["Three strategies"](https://github.com/hamlett-neil-ur/ahp-graph-entropy/blob/main/research-paper/I%20am%20writing%20a%20formal%20paper%20that%20I%20would%20like%20to....gdoc) analysis.
* Select peer-reviewed journal and submit.


# GitHub mechanics 🔧🔩🪛

## 1. Virtual-environment start-up.

#### a. Navigate to the project directory.

Navigate in the terminal window to the directory into which the repository was cloned.

```bash
cd '~/ahp-graph-entropy'
```

#### b. Bootstrap into anaconda.

```bash
source ~/.zshrc
```

#### c. Inintialize the environment based on the `environment.yml` specification.

```bash
conda env update --name ahp-graph-entropy --file environment.yml --prune
```

#### d. Activate the envoronment.

```bash
conda activate ahp-graph-entropy
```

#### e. Verify the configuration

```bash
python --version
which python
```

The expected responses resemble

```text
Python 3.11.15
~/anaconda3/envs/ahp-graph-entropy/bin/python
```


## 2. Commit management.

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

#### ⅴ. Push the commit.

```bash
git push --force-with-lease
```


### d. Consolidating commits to a branch (hard quash).

```bash
get fetch origin
git reset --soft $(git rev-list --max-parents=0 HEAD)
git commit --amend -m "Consolidated commit message"
git push --force-with-lease
```


### e. Remove previously-staged content from the online repository.


```bash
git rm -r --cached research-materials
git commit -m "Untrack research-materials directory and enforce .gitignore"
git push origin main
```
