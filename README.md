# Evidentiary reasoning with the Analytic Hierarchy Process: Use of graph entropy to rank decision factors

## Abstract.

 Decision makers often require insight into the relative strength of the elements of evidence on which their choices hinge. The Analytic Hierarchy Process (AHP) contains innate mechanisms leading to the rigorous quantification of elements' relative strength. Comparative judgements (“pairwise comparisons”) between elements of a given hierarchy model produce lists of edges for a complete graph. Under certain conditions, such graphs are also directed and acyclic, belonging to the class of tournament graphs. Intensities of Importance from comparative judgements provide weights for graphs' edges. Relative-entropy calculations based on Laplacian matrices for induced subgraphs quantify the relative evidentiary strength associated with the decisional evidence ommitted from them. Motivated by quantum-computing research, recent innovations in matrix representations of graphs support the idiosyncratic structures arising from comparative judgements. A previously published case study related to an offshore-pipeline material selection demonstrates the approach ([`Zheng, et al` (2005)](https://doi.org/10.1016/j.ijpvp.2025.105461)). The graph-entropy method provides greater strength-of-contribution contrast than sensitivity analysis from the case study.


## Draft research paper. 📝 

[`260710-ahp-graph-entropy.pdf`](./research-paper/260711-ahp-graph-entropy.pdf).

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

The AHP formulation superficially resembles that of the canonical *decision problem under uncertainty* (d.p.u.u.) representing the departure point by [`Luce & Raiffa (1957), chapter 13`](https://store.doverpublications.com/products/9780486659435). 

* [`Luce & Raiffa (1957)`](https://store.doverpublications.com/products/9780486659435). Consider a Cartesian product {(𝐴<sub>i</sub>, 𝑆<sub>j</sub>)} of acts 𝐴<sub>i</sub> performed given a specific decision and unknown states of nature 𝑆<sub>j</sub>. Which 𝑆<sub>j</sub> corresponds to the actual ontic state 𝑆<sup>ont</sup> represents the essential aspect of uncertainty. A utility mapping 𝑢<sub>i,j</sub> ↤ 𝒰(𝐴<sub>i</sub>, 𝑆<sub>j</sub>) for utility function 𝒰 provides the objective to be optimized. We seek a decision rule to find 𝓊<sup>opt</sup>=max<sub>i,j</sub>{𝑢<sub>i,j</sub>}.

* With AHP (and MAUT) we begin with a set of decision elements ℌ⊇{𝑒₁,⋯,𝑒<sub>𝑁</sub>} for hierarchy model ℌ. Moreover we have a set of options 𝒪⊇{ℴ₁,⋯,𝑜<sub>𝑀</sub>} from which to select. We also have a matrix of measurements  𝑹<sub>ℌ</sub>=[𝒓₁ ⋯ 𝒓<sub>𝑁</sub>], within which each column 𝒓<sub>𝑛</sub> is a vector of measurements for each ℴ<sub>𝑚</sub>∈𝒪 with respect to the 𝑛<sup>th</sup> element in ℌ. We standardize 𝑹<sub>ℌ</sub> to obtain 𝑷<sub>ℌ</sub>, and as in (12b) of [`260528-ahp-graph-entropy.pdf`](https://drive.google.com/file/d/1BR45AW378_d-EXYlBj00NM6JgoaBYdBb), our utility-optimization operation becomes 𝒑<sub>target</sub>=(𝑷<sub>ℌ</sub>⊗𝜴<sub>ℌ</sub>)𝝎<sub>target</sub>.

These are qualitatively different problems. Our plausible states of nature {𝑆<sub>j</sub>} are categorically different from our preference-ordering element measurements {𝒓<sub>𝑛</sub>}, and their standardized equivalents {𝒑<sub>𝑛</sub>}. We must address the following.

1. Formulate the argument that [`Luce's & Raiffa's (1957)`](https://store.doverpublications.com/products/9780486659435) axioms for d.m.u.u. represent a valid logic for preferential ordering of options given element measurements and comparative judgements about elements' relative importances with respect to each other.
2. Demonstrate that widely perceived logical deficiencies in AHP do not inescapably trap one in a state of irrationality. The most-obvious perceived deficiencies include:

    a. **Use of the "universal scale" in comparative judgements** ([`Saaty (2001b)`](https://doi.org/10.13033/isahp.y2001.030)). We argue alternatively for personal-probability-based approach to assigning intensities of importance during comparative judgement.

    b. **Rank reversal upon introduction of new options**. We dispel the perception that rank-reversal mysteriously arises from aberrant approaches to priority-vector calculations. This violates foundational principles of *Linear Time-Invariant* (LTI) systems. Alternatively, rank-reversal can arise upon introduction of an additional option ℴ' for which one or more hierachy-model elements 𝑟<sub>𝑛</sub>' falls outside of the measured range of previously observed element measurements 𝑟<sub>𝑛</sub>' ∉ [min(𝒓<sub>𝑛</sub>), max(𝒓<sub>𝑛</sub>)]. If this occurs, it is inconsequential provided that ℴ'⊁ℴ<sup>opt</sup>∈𝒪.


#### Preferential ordering versus utility.

As of commit [`735d77f96fd192ecdce3a2ecd11c35cd05bf49b4`](https://github.com/hamlett-neil-ur/ahp-graph-entropy/tree/735d77f96fd192ecdce3a2ecd11c35cd05bf49b4), the case study focuses on the mechanics of AHP. Given the title and objective, some mention of the epistemology of AHP seems called-for. Spefically, AHP focuses on "prioritized" ordering, in contrast with utility-optimization of mainstream decision theory. [Saaty (2001a)](https://doi.org/10.13033/isahp.y2001.029) seemingly differentiates AHP from *utility theory*, positioning as a distinct logical paradigm. The dearth of AHP-related articles in INFORMS [*Decision Analysis*](https://pubsonline.informs.org/journal/deca) seems to corroborate the hypothesis of a schism. [Abbas' (2026)](https://www.decisionprofessionals.com/events/simple-registration?CalendarEventKey=bd2fb3d0-7aa0-4d4e-a38d-019d891f176e&Home=%2fsdp-participate%2fevents) seemingly categorical indictment of the irrationality of reasoning based on "pairwise comparisons" also fits the pattern.

Nonetheless, the strength-of-preference ordering ***p***<sub>target</sub> in (12b) of [`260528-ahp-graph-entropy.pdf`](https://drive.google.com/file/d/1BR45AW378_d-EXYlBj00NM6JgoaBYdBb) resembles quantities characterized as *utilities* in, e.g., Multi-Attribute Utility Theory (MAUT).  Following [`Pettigrew's (2016)`](https://global.oup.com/academic/product/accuracy-and-the-laws-of-credence-9780198732716) reasoning, "A utility function 𝒰 ... takes an option ℴ [from option set 𝒪] and a world 𝓌 from [palusible ontic states] 𝒲 and returs a real number 𝒰(ℴ,𝓌) that measures ... the utility of ℴ at 𝓌." Seemingly a strength-of-preference [***p***<sub>target</sub>]<sub>i</sub> can be framed in these terms. Note that [`Pettigrew's (2016)`](https://global.oup.com/academic/product/accuracy-and-the-laws-of-credence-9780198732716) framing exactly corresponds to [`Luce & Raiffa (1985), §13.3`](https://store.doverpublications.com/products/9780486659435).

#### Rank reversal by AHP.

The occurrence of rank reversal appears to form the basis for, e.g., [Abbas' (2026)](https://www.decisionprofessionals.com/events/simple-registration?CalendarEventKey=bd2fb3d0-7aa0-4d4e-a38d-019d891f176e&Home=%2fsdp-participate%2fevents) categorical castigation of decision-making methods based pairwise comparisons. [Abbas (2026)](https://www.decisionprofessionals.com/events/simple-registration?CalendarEventKey=bd2fb3d0-7aa0-4d4e-a38d-019d891f176e&Home=%2fsdp-participate%2fevents) did not single out MAUT or AHP. He referred to parwise comparisons employed within the context of Gaussian cupolas (e.g., [Haugh (2016)](https://www.columbia.edu/~mh2078/QRM/Copulas.pdf)), apparently a contributor to catastrophic financial-modeling failures associated with the financial crisis of the late 2000s.

##### Mechanisms leading to rank reversal.

Now, the rank-reversal dilemma bears consideration from two perspectives. First, [`Saaty, e.g., (2001a)`](https://doi.org/10.13033/isahp.y2001.029) made some amount of hubbub about the sensitivity of preferential ordering to the manner by which the priority vector 𝞈<sub>ℌ</sub> is calculated. We observe in [`260528-ahp-graph-entropy.pdf`](https://drive.google.com/file/d/1BR45AW378_d-EXYlBj00NM6JgoaBYdBb) that — using [`Pettigrew's (2016)`](https://global.oup.com/academic/product/accuracy-and-the-laws-of-credence-9780198732716) notation — adding another option ℴ' to 𝒪 can lead to re-normalization of the element-measurement matrix 𝑷<sub>ℌ</sub>, (11e) in [`260528-ahp-graph-entropy.pdf`](https://drive.google.com/file/d/1BR45AW378_d-EXYlBj00NM6JgoaBYdBb). This occurs specifically if any of the element measurements for ℴ' fall outside the range of those previously observed in 𝒪. The rub, then, seems to arise from coupling between the utility function and decision-element measurements.

When this occurs, our utility function 𝒰(ℴ,𝓌) has effectively changed: 𝒰'(ℴ,𝓌) ≠ 𝒰(ℴ,𝓌), where 𝒰' is based on 𝒪' = 𝒪⋃{ℴ'}. So then, does a non-preffered approach to calculating 𝞈<sub>ℌ</sub> induce rank reversal? Or does the phenomenon occur because re-standardization of decision-element measurements leads to 𝒰'|𝒪'≠𝒰|𝒪? That 𝞈<sub>ℌ</sub>∈Δ<sup>n</sup>, where Δ<sup>n</sup> denotes the unit simplex, would cause rank reversal seems to violate principles of *Linear Time-Invariant* (LTI) systems theory ([`Strum & Kirk (1988)`](https://lccn.loc.gov/86026542); [`Therrien (1992)`](https://lccn.loc.gov/91031057); [`Keesman (2011)`](https://doi.org/10.1007/978-0-85729-522-4); [`Proakis & Manolakis (2024)`](https://www.pearson.com/en-us/subject-catalog/p/digital-signal-processing-principles-algorithms-and-applications/P200000003415/9780137348657)).


##### Consequences of rank-reversal for rationality.

[`Saaty, e.g., (2001a)`](https://doi.org/10.13033/isahp.y2001.029) observes equivocation by [`Luce & Raiffa (1985), §13.3`](https://store.doverpublications.com/products/9780486659435) regarding rank-preservation order. Tha latter spoke to the effect of adding ℴ' to 𝒪. The core axiom of interest asserts that, "If an [option] is non-optimal ..., it cannot be made optimal by adding new [options]." The ordering of non-optimal options 𝒪 upon incorporation of a new option ℴ' does not affect the optimality of ℴ<sup>opt</sup>∈𝒪⊂𝒪' provided that ℴ'⊁ℴ<sup>opt</sup>.



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
