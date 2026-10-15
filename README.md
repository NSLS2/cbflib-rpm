# CBFlib RPM

RPM packaging for [CBFlib](https://github.com/dials/cbflib).

To create an rpm/srm, simply use the included makefile running:

```bash
make rpm
```

and 

```bash
make srpm
```

respectively.

This repository is based on the [NSLS2 standard RPM packaging template](https://github.com/NSLS2/rpm-repo-template). To update the template to the most recent version, run:

```bash
pixi run copier update
```

Note that you may need to resolve merge conflicts after updating.
