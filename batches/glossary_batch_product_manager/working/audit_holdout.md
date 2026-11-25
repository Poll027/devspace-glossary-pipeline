---
title: Holdout groups
description: "Create holdout groups in Amplitude Experiment to exclude users from experiments and measure the long-term, combined impact of your rollouts."
product: experiment
lang: en
last_updated: 2026-10-21
token_estimate: 1845
---
# Holdout groups

Sometimes you need to prevent a percentage of users from viewing an experiment. This matters most when you measure the long-term, combined effects of multiple experiments. Statistical significance in one experiment may not reflect the true, cumulative impact of your experimentation program.

> For AI agents: a documentation index is available at [/docs/llms.txt](/docs/llms.txt). Append `.md` to any page URL for markdown, or send `Accept: text/markdown`.

To exclude users from your experiments, create a holdout group. Holdout groups measure the long-term impact of your rolled-out variants and the lift of your experimentation program as a whole. A holdout group retains a set of users from previous experiments and shows them the winning combinations of past results. This group then gives you true measures of success for your previous experiments.

Your holdout groups experience previous experiments. You can set up dependencies that control which experiments the holdout group sees. For more information, go to [Flag dependencies](https://amplitude.com/docs/feature-experiment/under-the-hood/flag-dependencies#holdout-groups).

## Plan availability

Holdout groups is available as an add-on on the Growth and Enterprise plans. Go to [Amplitude pricing](https://amplitude.com/pricing) for plan details.

| Plan | Allowance | How to access |
| --- | --- | --- |
| Free | Not included | [Upgrade your plan](https://amplitude.com/pricing) |
| Plus | Not included | [Upgrade your plan](https://amplitude.com/pricing) |
| Growth | Not included | Available as an add-on. |
| Enterprise | Not included | Available as an add-on. |

_Availability reflects the latest Amplitude plans. If your organization is on an older plan, your access may differ. Check your plan under [Plans & Billing in your organization settings](/docs/admin/account-management/account-settings#organizational-settings), or contact your Amplitude account representative._

## Create a holdout group

> **Note:**
>
> Holdout groups can contain a mix of web experiments and feature experiments.

When you use holdout groups, note the following:

- **Set the holdout percentage between 1% and 10%**: Withholding a significant part of your total traffic can extend the time your experiments need to reach a conclusion.
- **Add experiments to a holdout group before they start running**: Adding running experiments to a holdout group can compromise the integrity of your data because Amplitude unassigns users from the active experiments.
- **Don't remove a running experiment from a holdout group**: Removing a running experiment compromises the integrity of your data because Amplitude assigns users to the active experiments.
- **Don't delete a holdout group with running experiments**: To protect your running experiment's data, delete the holdout group after all experiments in the group conclude.

##### To create a holdout group

1. In the Experiment functionality, go to _Experiments > Mutex and Holdouts tab_.
2. To add a new holdout group to your project, click **Add a new holdout group**.

   - If you have existing groups, click **Create A New Group**, and then select **Holdout Group**.
3. In the Holdout group settings modal, enter the name, description, and holdout percentage for the group. You can also view and change advanced settings such as the evaluation mode and bucketing key of your group.

> **Note:**
>
> You can't change the holdout percentage after you create a group. This restriction ensures consistent bucketing and a consistent user experience.

4. Click **Add Experiment** to add experiments to your holdout group.
5. (_Optional_) Specify individuals or cohorts to include in or exclude from your holdout group. From either the Individuals or Cohorts tabs, add a user or cohort under _Include in holdout_ or _Exclude from holdout_. This option ensures that Amplitude always holds out or never holds out specific users from the holdout group.

Don't add the same users or cohorts to both the _Include a holdout_ and _Exclude from holdout_ slots. The _Include a holdout_ slot determines inclusion.

6. Click **Add Group** to finish the process.

## Manage holdout groups

Manage your holdout groups from the Experiment Groups tab or from within an experiment:

1. In the Mutex and Holdout tab, scroll down the table until you find the group you want to edit.
2. Click the **edit** icon.
3. Make your changes in the Holdout group settings modal and click **Save**.

If you're within an experiment that's part of a holdout group, follow these steps:

1. Click the name of the group you want to edit.
2. Make your changes in the Holdout group settings modal and click **Save**.

## Analyze a holdout group

Analyze your holdout groups using an Experiment Results chart.

##### To create a pre-populated Experiment Results chart

1. Navigate to the Experiments page and click the **Mutex and Holdout** tab.
2. Find the holdout group you want to analyze and click the **Analyze** icon.
3. Click **Open in Chart**.
4. A new Experiment Results chart opens, with the following fields complete:

   - Exposure event
   - Segments for `Holdout` and `On`
   - Statistical method set to [T-test](https://amplitude.com/docs/feature-experiment/experiment-theory/analyze-with-t-test) (_Samples per variant needed_ set to 10,000)
   - Analysis date range
5. From here, select the primary metric and start analyzing the impact of your holdout group.

## Advanced use cases

### Streamline multiple experiments and holdout groups

Adding an experiment to multiple holdout groups can limit the experiment's traffic. Experiment evaluates each user for each holdout group they belong to.

For example, you have the following two holdout groups:

- **Holdout group 1**: This group contains Experiment A and Experiment B, with a holdout percentage of 5%.
- **Holdout group 2**: The second group contains Experiment A and Experiment C, also with a holdout percentage of 5%.

Because Experiment A is part of both holdout groups (1 and 2), it receives the majority of the total traffic, or `0.95 * 0.95 = 0.9025` (90.25%).

Instead of adding an experiment to multiple holdout groups, create a single group with all the relevant experiments. A single group distributes traffic more evenly across experiments.

In the example above, you create one holdout group that contains all three experiments (A, B, and C).

### Manage experiments with holdout groups and mutual exclusion

Adding an experiment to a holdout group and a mutual exclusion group further limits the amount of traffic to the experiment. Experiment evaluates each user for both the holdout group and the mutual exclusion group.

For example, consider the following holdout group and mutual exclusion group:

- **The holdout group** has a holdout percentage of 5% and contains Experiment A.
- **The mutual exclusion group** directs half the traffic to Experiment A in slot 1, and the other half to Experiment B in slot 2.

In this scenario, Experiment A receives about half of the total traffic, or `0.95 * 0.5 = 0.475` (47.5%).

You can use holdout groups with mutual exclusion, but watch for the potential traffic limits as you plan and roll out your experiments.

For more information, refer to [mutual exclusion groups](https://amplitude.com/docs/feature-experiment/advanced-techniques/mutually-exclusive-experiments).

