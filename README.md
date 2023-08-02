### Task Manager
[![Actions Status](https://github.com/tatapestova/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/tatapestova/python-project-52/actions)
[![Lint check](https://github.com/tatapestova/python-project-52/actions/workflows/lint_check.yml/badge.svg)](https://github.com/tatapestova/python-project-52/actions/workflows/lint_check.yml)
[![Tests check](https://github.com/tatapestova/python-project-52/actions/workflows/tests_check.yml/badge.svg)](https://github.com/tatapestova/python-project-52/actions/workflows/tests_check.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/c72cfe3f892711fd3f12/maintainability)](https://codeclimate.com/github/tatapestova/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c72cfe3f892711fd3f12/test_coverage)](https://codeclimate.com/github/tatapestova/python-project-52/test_coverage)

Task Manager is a task management system similar to http://www.redmine.org/. It allows you to create tasks, assign performers, and change their statuses. To work with the system, registration and authentication are required.

![Registration](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjA2MmRhY2Q0NGJhOTEyMTI0YzczNjczNTA1NWEwMjYyLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=6de3fae52960e186127e416b86d453bd6d0416243493c5c4f8eab3de5e03c71c)

![Main page](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjgwNmYxMDBlY2M5YzM2ODE5NWRjYzllNjAxYzc0OTAwLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=495d87da299993c26e4578fce7e1c89ea8475727bdbfad84466a6aa5c65e455a)

![List of tasks](https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjJjM2JhNjVhMTZlMDY2MDg5NTMxYjQ5MjZkN2JhZjcxLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=b67c82a967fa2747aad3533126231e9da34f3f4d3425ccb6b8adcdf510e7dbd3)

### For local deployment
1. Clone repository.
```
git clone https://github.com/tatapestova/python-project-52.git
```
2. Add dependencies
```
make install
```
3. Set up DATABASE_URL and SECRET_KEY in the new .env file. and place it in the root of the project. 

4. Then this command will be available for local deployment.
```
make run
```