# Platform and framework sources

## TikTok platform context

1. TikTok. “How TikTok Recommends Content.” TikTok Support. https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content
   - **Informs:** the deployed referent (TikTok's For You feed) and the choice to represent user interactions as recommendation signals.
   - **Access:** public official support documentation, accessed 2026-11-05.
   - **Status/limit:** platform-authored description. It identifies multiple signal groups, including user interactions, content information, and user information; it does not disclose the complete ranking algorithm or numeric weights.

2. TikTok. “Manage Topics.” TikTok Support. https://support.tiktok.com/en/account-and-privacy/account-privacy-settings/manage-topics
   - **Informs:** the use of researcher-defined content-topic categories as a simplified model attribute.
   - **Access:** public official support documentation, accessed 2026-11-05.
   - **Status/limit:** platform documentation mentions topic groupings such as sports, food and drinks, and lifestyle. The six categories in this model are a researcher-defined set, not TikTok's official complete taxonomy.

## Mesa framework and preserved source example

3. Mesa Team. “Creating Your First Model — The Boltzmann Wealth Model.” Mesa documentation. https://mesa.readthedocs.io/stable/tutorials/0_first_model.html
   - **Informs:** the preserved starter model and basic use of Mesa `Agent`, `Model`, agent activation, and seeded random behaviour.
   - **Access:** public official Mesa documentation, accessed 2026-11-05.
   - **Status/limit:** official tutorial code, retained separately under `src/boltzmann_wealth_model/`.

4. Mesa. “Mesa: Agent-based modeling in Python.” PyPI. https://pypi.org/project/Mesa/3.5.2/
   - **Informs:** the pinned Mesa version for the prototype environment.
   - **Access:** public package metadata, accessed 2026-11-05.
   - **Status/limit:** PyPI lists Mesa 3.5.2 as the latest stable release on the access date and specifies Python 3.12 or newer.

## Model assumptions not supplied by these sources

The 120 synthetic videos, six balanced categories, baseline score distribution, initial preference scores, engagement probability formula, preference increment, personalization weights, feed size, and 20-round run length are project modelling decisions. They are not measurements or disclosed settings from TikTok.
