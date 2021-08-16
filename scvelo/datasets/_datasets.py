import warnings

import numpy as np
import pandas as pd

from scanpy import read

from scvelo.core import cleanup
from scvelo.read_load import load

url_datadir = "https://github.com/theislab/scvelo_notebooks/raw/master/"


def toy_data(n_obs=None):
    """
    Randomly sampled from the Dentate Gyrus dataset.

    Arguments
    ---------
    n_obs: `int` (default: `None`)
        Size of the sampled dataset

    Returns
    -------
    Returns `adata` object
    """

    adata_dg = dentategyrus()

    if n_obs is not None:
        indices = np.random.choice(adata_dg.n_obs, n_obs)
        adata = adata_dg[indices]
    else:
        adata = adata_dg
    adata.obs_names_make_unique()
    return adata.copy()


def dentategyrus(adjusted=True):
    """Dentate Gyrus neurogenesis.

    Data from `Hochgerner et al. (2018) <https://doi.org/10.1038/s41593-017-0056-2>`_.

    Dentate gyrus (DG) is part of the hippocampus involved in learning, episodic memory
    formation and spatial coding. The experiment from the developing DG comprises two
    time points (P12 and P35) measured using droplet-based scRNA-seq
    (10x Genomics Chromium).

    The dominating structure is the granule cell lineage, in which neuroblasts develop
    into granule cells. Simultaneously, the remaining population forms distinct cell
    types that are fully differentiated (e.g. Cajal-Retzius cells) or cell types that
    form a sub-lineage (e.g. GABA cells).

    .. image:: https://user-images.githubusercontent.com/31883718/79433223-255b8700-7fcd-11ea-8ecf-3dc9eb1a6159.png
       :width: 600px

    Returns
    -------
    Returns `adata` object
    """  # noqa E501

    if adjusted:
        filename = "data/DentateGyrus/10X43_1.h5ad"
        url = f"{url_datadir}data/DentateGyrus/10X43_1.h5ad"
        adata = read(filename, backup_url=url, sparse=True, cache=True)

    else:
        filename = "data/DentateGyrus/10X43_1.loom"
        url = "http://pklab.med.harvard.edu/velocyto/DG1/10X43_1.loom"
        adata = read(filename, backup_url=url, cleanup=True, sparse=True, cache=True)
        cleanup(adata, clean="all", keep={"spliced", "unspliced", "ambiguous"})

        url_louvain = f"{url_datadir}data/DentateGyrus/DG_clusters.npy"
        url_umap = f"{url_datadir}data/DentateGyrus/DG_umap.npy"

        adata.obs["clusters"] = load(
            "./data/DentateGyrus/DG_clusters.npy", url_louvain, allow_pickle=True
        )
        adata.obsm["X_umap"] = load(
            "./data/DentateGyrus/DG_umap.npy", url_umap, allow_pickle=True
        )

        adata.obs["clusters"] = pd.Categorical(adata.obs["clusters"])

    return adata


def forebrain():
    """Developing human forebrain.

    Forebrain tissue of a week 10 embryo, focusing on glutamatergic neuronal lineage.

    Returns
    -------
    Returns `adata` object
    """

    filename = "data/ForebrainGlut/hgForebrainGlut.loom"
    url = "http://pklab.med.harvard.edu/velocyto/hgForebrainGlut/hgForebrainGlut.loom"
    adata = read(filename, backup_url=url, cleanup=True, sparse=True, cache=True)
    adata.var_names_make_unique()
    return adata


def pancreas():
    """Pancreatic endocrinogenesis

    Data from `Bastidas-Ponce et al. (2019) <https://doi.org/10.1242/dev.173849>`_.

    Pancreatic epithelial and Ngn3-Venus fusion (NVF) cells during secondary transition
    with transcriptome profiles sampled from embryonic day 15.5.

    Endocrine cells are derived from endocrine progenitors located in the pancreatic
    epithelium. Endocrine commitment terminates in four major fates: glucagon- producing
    α-cells, insulin-producing β-cells, somatostatin-producing δ-cells and
    ghrelin-producing ε-cells.

    .. image:: https://user-images.githubusercontent.com/31883718/67709134-a0989480-f9bd-11e9-8ae6-f6391f5d95a0.png
       :width: 600px

    Returns
    -------
    Returns `adata` object
    """  # noqa E501

    filename = "data/Pancreas/endocrinogenesis_day15.h5ad"
    url = f"{url_datadir}data/Pancreas/endocrinogenesis_day15.h5ad"
    adata = read(filename, backup_url=url, sparse=True, cache=True)
    adata.var_names_make_unique()
    return adata


def pancreatic_endocrinogenesis():
    warnings.warn(
        "`scvelo.datasets.pancreatic_endocrinogenesis` is deprecated since scVelo "
        "v0.2.4 and will be removed in a future version. Please use "
        "`scvelo.datasets.pancreas` instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return pancreas()