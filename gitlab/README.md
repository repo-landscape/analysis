# GitLab API harvesting tools

 * To produce the up to date content of the data directory run:
  ```bash
  python3 acdh_gitlab_repos.py {apiKey} projects.csv --endpoint projects --format csv
  python3 acdh_gitlab_repos.py {apiKey} users.csv --endpoint members/all --format csv
  python3 acdh_gitlab_repos.py {apiKey} events.csv --endpoint events --format csv
  ```
* `acdh_gitlab_repos.Rmd` contains simple data analysis in R
* `acdh_gitlab_repos.html` is compiled version of the `acdh_gitlab_repos.Rmd`

