import os
import git
import logging
import pandas as pd
from interface.utilities.load_config import RepositoryConfig, ArtifactConfig


class ProcessGitLocal():
    """
    Local Repository data Analysis
    """
    def __init__(self, repo_config: RepositoryConfig, artf_config: ArtifactConfig):
        self.repo_config = repo_config
        self.artf_config = artf_config
        self.repo = git.Repo(repo_config.localrepo, odbt=git.GitCmdObjectDB)
        self._logger = logging.getLogger(__name__)

    def construct_dataframe(self):
        """
        Construction of required columns
        """
        try:    
            commits = pd.DataFrame(
                self.repo.iter_commits('master'), columns=['raw'])
            commits['author'] = commits['raw'].apply(lambda x: x.author.name)
            # commits['email'] = commits['raw'].apply(lambda x: x.author.email)
            commits['committed_date'] = commits['raw'].apply(
                lambda x: pd.to_datetime(x.committed_datetime, utc=True))
            commits['commit_date'] = commits['committed_date'].dt.date
            commits['commit_year'] = commits['committed_date'].dt.year
            commits['commit_hour'] = commits['committed_date'].dt.hour
            commits['commit_month'] = commits['committed_date'].dt.month
            # commits['message'] = commits['raw'].apply(lambda x: x.message)
            # Keeping Raw column to calculate the file count
            commits['sha'] = commits['raw'].apply(lambda x: str(x))
            return commits
        except Exception as diag:
            return f"Dataframe halted {diag}"

    # As larger repository grows the calculation of file stats
    # from each commits adds up computaion time
    def formation_of_data(self, commits: pd.DataFrame):
        """
        Formation of statistics dict
        """     
        stats = pd.DataFrame(commits['raw'].apply(
            lambda x: pd.Series(x.stats.files)).stack()).reset_index(
                level=1)
        stats = stats.rename(
            columns={'level_1': 'filename', 0: 'stats_modifications'})
        stats_modifications = stats['stats_modifications'].apply(
            lambda x: pd.Series(x))
        stats = stats.join(stats_modifications)
        del(stats['stats_modifications'])
        commits = commits.join(stats)
        del(commits['raw'])

        df = pd.DataFrame([{
            "total_artifact": len(commits[commits['filename'].str.contains(
                                self.artf_config.artifactstart)].filename.unique()),
            "total_commits": len(commits),
            "total_commiter": commits.author.unique().size,
            "current_month_commits": len(
                commits[(commits.commit_month == pd.to_datetime('now').month) & (commits.commit_year == pd.to_datetime('now').year)])
        }])

        # Day wise commit chart
        commits_by_date = commits.groupby('commit_date')[['sha']].count()
        commits_by_date = commits_by_date.rename(columns={'sha':'commit_count'})
        commits_by_date.reset_index(level=0, inplace=True)
        
        # Day wise commit chart
        commits_by_month = commits.groupby('commit_month')[['sha']].count()
        commits_by_month = commits_by_month.rename(columns={'sha':'commit_count'})
        commits_by_month.reset_index(level=0, inplace=True)
        
        # Total Commit year wise
        commits_by_year = commits.groupby('commit_year')[['sha']].count()
        commits_by_year = commits_by_year.rename(
            columns={'sha': 'commit_count'})
        commits_by_year.reset_index(level=0, inplace=True)

        # Total Commits Hour wise
        commits_by_hour = commits.groupby('commit_hour')[['sha']].count()
        commits_by_hour = commits_by_hour.rename(columns={'sha':'commit_count'})
        commits_by_hour.reset_index(level=0, inplace=True)

        return {
            'dataframe': df,
            'date_dataframe': commits_by_date,
            'hour_dataframe': commits_by_hour, 
            'year_dataframe': commits_by_year,
            'month_dataframe': commits_by_month
        }

    def between_date_analysis(
        self, df: pd.DataFrame, start_date: str,
        end_date: str):
        """
        Return Group by dataframe based of year and month
        """
        commits = df[(df.committed_date > start_date) & (df.committed_date <= end_date)]
        stats = pd.DataFrame(commits['raw'].apply(
            lambda x: pd.Series(x.stats.total.get('files'))).stack()).reset_index(level=1)
        stats = stats.rename(columns={0: 'File_Count'})
        commits = commits.join(stats)
        commits.drop(['commit_hour', 'sha', 'level_1', 'commit_date'], axis="columns", inplace=True)
        file_count = commits.groupby([
            commits.commit_year,
            commits.commit_month,
            commits.author], as_index=False).agg({'sum'}).reset_index()
        commit_count = commits.groupby([
            commits.commit_year,
            commits.commit_month,
            commits.author], as_index=False).agg({'count'}).reset_index()
        df1 = pd.DataFrame(commit_count[['commit_year', 'commit_month', 'author', 'raw']])
        df2 = pd.DataFrame(file_count[['commit_year', 'commit_month', 'author', 'File_Count']])
        return pd.merge(df1, df2)

    def year_month_analysis(self, df: pd.DataFrame, year, month):
        """
        Return Group by dataframe based of year and month
        """
        df_return = df[(df.commit_year == year) & ( df.commit_month == month)]
        return df_return