# MINA: A coreference evaluation tool using both maximum and minimum spans

We provide the implementation of the common evaluation metrics including MUC, B-cubed, CEAFe, and LEA.
Apart from the standard setting that evaluates coreferring mentions according to the maximum logical span of mentions,
we also provide minimum span evaluations in which minimum spans are extracted using the MINA algorithm.
If gold parse trees are annotated in the key file, MINA uses gold syntactic parse information to extract minimum spans.
Otherwise, it uses the Stanford English PCFG parser to parse the key file. 

### Requirement

This evaluation tool requires numpy, scipy, and scikit-learn packages.

## Usage

The following command evaluates coreference outputs related to the ARRAU dataset:

python arrau-scorer.py <key> <system> [options]

<Key> is either a key file or a directory that contains key files. The script only processes the key files that end with .CONLL. If <key> is a directory, the script recursively looks for all .CONLL files that are located in <key> or one of its subdirectories.

<system> is either a system generated coreference output or a directory that contains coreference output files. All system file names should also end with .CONLL. 

## Evaluation Metrics

The above command reports MUC [Vilain et al, 1995], B-cubed [Bagga and Baldwin, 1998], CEAFe [Luo et al., 2005], LEA [Moosavi and Strube, 2016] and the averaged CoNLL score (the average of the F1 values of MUC, B-cubed and CEAFe) [Denis and Baldridge, 2009a; Pradhan  et  al., 2011].

You can also only select specific metrics by including one or some of the 'muc', 'bcub', 'ceafe' and 'lea' options in the input arguments.
For instance, the following command only reports the CEAFe and LEA scores:

python arrau-scorer.py <key> <system> ceafe lea

The first and second arguments after "arrau-scorer.py" have to be <key> and <system>, respectively. The order of other options is arbitrary. 

## Evaluation Modes

Apart from coreference relations, the ARRAU dataset also contains annotations for singletons and non-referring markables. Non-referring markables are annotated with the "non_referring" tag and are therefore distinguishable from referring markables (coreferent markables or singletons). 
After extracting all markables, all markables whose corresponding coreference chain is of size one, are specified as singletons.
By distinguishing coreferent markables, singletons and non-referring markables, we can perform coreference evaluations in various settings by using the following two options:

1) remove_singletons:  if this option is included in the command, all singletons in the key and system files will be excluded from the evaluation. 
The handling of singletons 

2) keep_non_referring:  if this option is included in the command, all markables that are annotated as non_referring, both in the key and system files, will be included in the evaluation.
If this option is included, separate recall, precision, and F1 scores would be reported for identifying the annotated non-referring markables.

As a result, if you only run "python arrau-scorer.py <key> <system>" without any additional options, the evaluation is performed by incorporating all coreferent and singleton markables and without considering non-referring markables.

Overall, above options enable the following evaluation modes:

# Evaluating coreference relations only

This evaluation mode is compatible with the coreference evaluation of the OntoNotes dataset in which only coreferring markables are evaluated.
To do so, the remove_singletons option should be included in the evaluation command:

python arrau-scorer.py <key> <system> remove_singletons

In this mode, all singletons and non-referring mentions will be skipped from coreference evaluations.

# Evaluating coreference relations and singletons 

This is the default evaluation mode of the ARRAU dataset and its corresponding command is

python arrau-scorer.py <key> <system>

In this mode, both coreferring markables and singletons are evaluated by the specified evaluation metrics.
Apart from the MUC metric, all other evaluation metrics handle singletons.
The only case in which MUC handles singletons is when they are incorrectly included in system detected coreference chains. In this case, MUC penalizes the output for including additional incorrect coreference relations. Otherwise, MUC does not handle, or in other words skip, markables that do not have coreference links. 
You can refer to Moosavi and Strube [2016] for more details about various evaluation metrics.

# Evaluating all markables 

In this evaluation setting, all specified markables including coreference, singleton, and non-referring mentions are taken in to account for evaluation.
The scores of coreference evaluation metrics would be the same as those of the above mode, i.e. evaluating coreference relations and singletons.
However, a separate score would be reported for identifying the annotated non-referring markables.

The following command performs coreference evaluation using this mode

python arrau-scorer.py <key> <system> keep_non_referring

 
## Minimum Span Evaluation

The ARRAU dataset contains a MIN attribute which indicates the minimum string that a coreference
resolver must identify for the corresponding markable.
For minimum span evaluation, a system detected boundary for a markable is considered as correct if it contains the MIN string and doesn't go beyond the annotated maximum boundary.

To perform minimum span evaluations, add one of the 'MIN', 'min' or 'min_spans' options to the input arguments.
For instance, the following command reports all standard evaluation metrics using minimum spans to specify markables instead of maximum spans:

python arrau-scorer.py <key> <system> min

