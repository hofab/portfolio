# portfolio
Simplest approach of tracking portfolios in python

## Setting up your virtual environment

I will base my setup on the recommendaitons found here:
https://mitelman.engineering/blog/python-best-practice/automating-python-best-practices-for-a-new-project/
by ALex Mitelman

1. Install pyenv
    curl https://pyenv.run | bash
or
    yay -Syu pyenv
2. Update to desired python version, 3.9.6 in my case
    pyenv install 3.9.6
3. Install poetry for dependency managment
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
4. Create new project with poetry
    poetry new <project.name>
or use existing project
    poetry init
6. Define what python version to use
    pyenv local 3.9.6
7. Use poetry to pick up current python version
    poetry env use python
8. Add packages to your environment
    poetry add <package-name>
    e.g. pytest
9. Create tests folder and file
    mkdir tests && cd tests && touch portfolio_tests.py
10. Execute your script
    poetry run python <filename>.py


