1) Build docker image


```
docker build -t ssh .
```


2) Export environment variables

```
export AWS_ACCESS_KEY_ID="ASIARI6PKILYB5VKZXK"                                        INT ✘ 
export AWS_SECRET_ACCESS_KEY="1UVqjHJ9liUL8tvtSSKZ0gqdbybkc+xlf356hrE"
export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2jEOD//////////wEaCXVzLXdlc3QtMiJHMEUCIQDw4dnHYysaJ1mAEnmCvElnwdCMDJ8/D3Dwe19J2F000gIgdA0d2Tqa/BEkGTf+dqRQUvQnSaIEkEOjQiCNFFRKmgUq+wIIeRAAGgwwODc5NDQ3NDE2MTYiDKmwJMWDxTjFKIYqMirYAkMQHRz2fRmQAM+hp3zVInKJ2P/LRXJP+qx4N9bOft2o/Ozw6UylbhQA6ouhGZNtIyguBSfSPY7M+lU7gt0pLgpJkN19G5/bVMpyfBQsLp8SeybWqEB3gDo19izLgOSeH/y2o3s+PU6Gq/JJtMIdImO1OoGLkBBLhkdGWOrZfQozFkxDd3YNqgHVC3ruN6UxPXbK6dO5Lo02ja8fNuJRDMAHuvBdFSwL7Ealu7CX013Vz6y0MQa2GXKN/dpucGeahyVm4IuCah2fxex8FuNdrFCCEr88dQY0CuwPblZKdABqtenGoQ4oITKL3q1sWmnLnAF3Urhp70lifKxnPV89+Y3cl8Tx5AJcdq/5aaH7YO6v/f3OCVimSrAHUzUvfld06xClvqSST3Dktnn9KHebZfur+auodFbOIkBCRFpkpDcanFelMJfJuHzWhB4IeH/YgzY5JQNpCQZMKyo26wGOqcBUqysdvg2s9iKm9kEpnVeYSx0oIsKzaEg8HmjlXNzQrxC5cTDNJzQpZrOaozjHIZTaAYH7V9xaSwwz7+yFYLLG6v0hE8oZwCyOP2euhO0T4SZhXhN2eKyXAs6kVwiseGsLxIJtgr6bZ4FGHo8rjsvWJotjdEbBe78EFNO8E1hWXKigXBH2moFvHbvyVjDleVz5AplBCpbgFeTj8f+8aUsnkNPXFlChzA="
export ENVIRONMENT=dev
export TARGET=rds
```

3) Run docker container

```
docker run -it --rm -e ENVIRONMENT -e TARGET -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN ssh
```