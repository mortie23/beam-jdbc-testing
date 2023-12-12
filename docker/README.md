# Building a custom Dataflow flex template

Working from this example here: 

[Using Flex Templates](https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates#local-shell)
[streaming_beam.py](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/dataflow/flex-templates/streaming_beam/streaming_beam.py)

## Options

### Manually build and create the flex template

This manual option may be required when you are working within a restricted VPC or enterprise environment where the cloud administrators have not given you certain required accesses.

You will need a GCP Artifact registry Docker repository.

Firstly manually build the Docker image on your local client development machine.
Tag the image with the full reference to the GCP Artifact registry.

```sh
docker build . -t australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:0.1
```

Before you try to push the container image to the container registry (in GCP this is called a Dcoker repository in a Artifact registry) you need to authenticate your `gcloud`` CLI with the artifact registry.

```sh
gcloud auth configure-docker australia-southeast1-docker.pkg.dev
```

Push the image to the registry.

```sh
docker push australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:0.1
```

Now we can build a flex template.

```sh
gcloud dataflow flex-template build "gs://bkt-flex-test/flex/hellofruit.json" \
     --image "australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:0.1" \
     --sdk-language "PYTHON" \
     --metadata-file "metadata.json"
```

This should run quite quickly and result in a JSON file in the bucket location you requested.

```log
Successfully saved container spec in flex template file.
Template File GCS Location: gs://bkt-flex-test/flex/hellofruit.json
Container Spec:

{
    "defaultEnvironment": {},
    "image": "australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:0.1",
    "metadata": {
        "description": "Hello fruit Python flex template.",
        "name": "Hello fruit",
        "parameters": [
            {
                "helpText": "Name of the BigQuery output table name.",
                "isOptional": true,
                "label": "BigQuery output table name.",
                "name": "output_table",
                "regexes": [
                    "([^:]+:)?[^.]+[.].+"
                ]
            }
        ]
    },
    "sdkInfo": {
        "language": "PYTHON"
    }
}
```

Cool, you can now test that you can use the custom template in Dataflow.
For this example you will need a BigQuery table ready.

```sql
create table flextest.hellofruit (
    name string
    , test_number int64
)
```

### Build the container and flex template together

This method will:

- do the `docker build` and `docker push` for you
- create a json file `Successfully saved container spec in flex template file.`

However, it uses GCP Cloud Build which needs to create it's own bucket called `<project-id>_cloudbuild` and does this in Multi-region US. Maybe you don't have the permissions in your enterprise to create new buckets or to create resources in certain regions.

```sh
gcloud dataflow flex-template build "gs://bkt-flex-test/flex/hellofruit.json" \
     --image-gcr-path "australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:latest" \
     --staging-location "gs://bkt-flex-test/flex/staging" \
     --temp-location "gs://bkt-flex-test/flex/tmp" \
     --gcs-log-dir "gs://bkt-flex-test/flex/log" \
     --sdk-language "PYTHON" \
     --flex-template-base-image "PYTHON3" \
     --metadata-file "metadata.json" \
     --py-path "." \
     --env "FLEX_TEMPLATE_PYTHON_PY_FILE=hellofruit.py" \
     --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=requirements.txt" \
     --log-http \
     --verbosity debug
```

The logs show the creation of the `_cloudbuild` bucket and the steps that build the container image, push it to the container registry and then create the template JSON file in the bucket.

```log
Copying files to a temp directory /tmp/tmp5wi9dy3r
Generating dockerfile to build the flex template container image...
Generated Dockerfile. Contents: 
FROM gcr.io/dataflow-templates-base/python3-template-launcher-base:latest

ENV FLEX_TEMPLATE_PYTHON_PY_FILE=/template/hellofruit.py
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=/template/requirements.txt

COPY docker /template/

RUN apt-get update && apt-get install -y libffi-dev git && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -U -r /template/requirements.txt

Creating temporary tarball archive of 6 file(s) totalling 4.3 KiB before compression.
Uploading tarball of [/tmp/tmp5wi9dy3r] to [gs://<project-id>_cloudbuild/source/1702341847.488544-472e119f8ea54ab58c7aba5d660434ff.tgz]
Pushing flex template container image to GCR...
Created [https://cloudbuild.googleapis.com/v1/projects/<project-id>/locations/global/builds/08d1100f-bfa1-4e0d-b440-4e63e76ba444].
Logs are available at [ https://console.cloud.google.com/cloud-build/builds/08d1100f-bfa1-4e0d-b440-4e63e76ba444?project=965889644844 ].
---------------------------------------------------------------------- REMOTE BUILD OUTPUT ----------------------------------------------------------------------
starting build "08d1100f-bfa1-4e0d-b440-4e63e76ba444"

FETCHSOURCE
Fetching storage object: gs://<project-id>_cloudbuild/source/1702341847.488544-472e119f8ea54ab58c7aba5d660434ff.tgz#1702341849496817
Copying gs://<project-id>_cloudbuild/source/1702341847.488544-472e119f8ea54ab58c7aba5d660434ff.tgz#1702341849496817...
/ [1 files][  2.2 KiB/  2.2 KiB]                                                
Operation completed over 1 objects/2.2 KiB.
BUILD
Already have image (with digest): gcr.io/cloud-builders/docker
Sending build context to Docker daemon  10.24kB
Step 1/5 : FROM gcr.io/dataflow-templates-base/python3-template-launcher-base:latest
latest: Pulling from dataflow-templates-base/python3-template-launcher-base
ca2b8d9337fc: Pulling fs layer
092157a61c6d: Pulling fs layer
864d9bbc0267: Pulling fs layer
b7b13f31af1a: Pulling fs layer
7ffb6cfa25b1: Pulling fs layer
a76de5baa185: Pulling fs layer
529909ed9b91: Pulling fs layer
30d2fb6a3137: Pulling fs layer
572906fd3287: Pulling fs layer
775492ce246a: Pulling fs layer
3481dbdd5b7a: Pulling fs layer
fc511350da18: Pulling fs layer
4a5417e16a2a: Pulling fs layer
c80082f0e835: Pulling fs layer
1c4d64c1d7a9: Pulling fs layer
9bbd5684e4d3: Pulling fs layer
b7b13f31af1a: Waiting
572906fd3287: Waiting
775492ce246a: Waiting
7ffb6cfa25b1: Waiting
a76de5baa185: Waiting
529909ed9b91: Waiting
30d2fb6a3137: Waiting
3481dbdd5b7a: Waiting
fc511350da18: Waiting
c80082f0e835: Waiting
1c4d64c1d7a9: Waiting
9bbd5684e4d3: Waiting
4a5417e16a2a: Waiting
092157a61c6d: Verifying Checksum
092157a61c6d: Download complete
b7b13f31af1a: Verifying Checksum
b7b13f31af1a: Download complete
864d9bbc0267: Verifying Checksum
864d9bbc0267: Download complete
7ffb6cfa25b1: Verifying Checksum
7ffb6cfa25b1: Download complete
ca2b8d9337fc: Verifying Checksum
ca2b8d9337fc: Download complete
a76de5baa185: Verifying Checksum
a76de5baa185: Download complete
572906fd3287: Verifying Checksum
572906fd3287: Download complete
775492ce246a: Verifying Checksum
775492ce246a: Download complete
3481dbdd5b7a: Verifying Checksum
3481dbdd5b7a: Download complete
fc511350da18: Verifying Checksum
fc511350da18: Download complete
4a5417e16a2a: Verifying Checksum
4a5417e16a2a: Download complete
529909ed9b91: Verifying Checksum
529909ed9b91: Download complete
1c4d64c1d7a9: Verifying Checksum
30d2fb6a3137: Verifying Checksum
30d2fb6a3137: Download complete
1c4d64c1d7a9: Download complete
9bbd5684e4d3: Verifying Checksum
9bbd5684e4d3: Download complete
c80082f0e835: Verifying Checksum
c80082f0e835: Download complete
ca2b8d9337fc: Pull complete
092157a61c6d: Pull complete
864d9bbc0267: Pull complete
b7b13f31af1a: Pull complete
7ffb6cfa25b1: Pull complete
a76de5baa185: Pull complete
529909ed9b91: Pull complete
30d2fb6a3137: Pull complete
572906fd3287: Pull complete
775492ce246a: Pull complete
3481dbdd5b7a: Pull complete
fc511350da18: Pull complete
4a5417e16a2a: Pull complete
c80082f0e835: Pull complete
1c4d64c1d7a9: Pull complete
9bbd5684e4d3: Pull complete
Digest: sha256:cd6cbd2592df3f76834466257f64ce4486f9c6522ca7deb432fbecbd42df47d4
Status: Downloaded newer image for gcr.io/dataflow-templates-base/python3-template-launcher-base:latest
 ---> 6197e2796423
Step 2/5 : ENV FLEX_TEMPLATE_PYTHON_PY_FILE=/template/hellofruit.py
 ---> Running in 10dd05a28bea
Removing intermediate container 10dd05a28bea
 ---> 83e973d1de61
Step 3/5 : ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=/template/requirements.txt
 ---> Running in 4f4d3460ea6d
Removing intermediate container 4f4d3460ea6d
 ---> aa8e3a8c7d95
Step 4/5 : COPY docker /template/
 ---> 128cc03a2391
Step 5/5 : RUN apt-get update && apt-get install -y libffi-dev git && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir -U -r /template/requirements.txt
 ---> Running in 25694eb09539
Get:1 http://deb.debian.org/debian bullseye InRelease [116 kB]
Get:2 http://deb.debian.org/debian-security bullseye-security InRelease [48.4 kB]
Get:3 http://deb.debian.org/debian bullseye-updates InRelease [44.1 kB]
Get:4 http://deb.debian.org/debian bullseye/main amd64 Packages [8062 kB]
Get:5 http://deb.debian.org/debian-security bullseye-security/main amd64 Packages [260 kB]
Get:6 http://deb.debian.org/debian bullseye-updates/main amd64 Packages [17.7 kB]
Fetched 8548 kB in 2s (5010 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  git-man less libbrotli1 libbsd0 libcbor0 libcurl3-gnutls libedit2
  liberror-perl libexpat1 libfido2-1 libgdbm-compat4 libgdbm6 libldap-2.4-2
  libldap-common libmd0 libnghttp2-14 libperl5.32 libpsl5 librtmp1 libsasl2-2
  libsasl2-modules libsasl2-modules-db libssh2-1 libx11-6 libx11-data libxau6
  libxcb1 libxdmcp6 libxext6 libxmuu1 netbase openssh-client patch perl
  perl-modules-5.32 publicsuffix xauth
Suggested packages:
  gettext-base git-daemon-run | git-daemon-sysvinit git-doc git-el git-email
  git-gui gitk gitweb git-cvs git-mediawiki git-svn gdbm-l10n sensible-utils
  libsasl2-modules-gssapi-mit | libsasl2-modules-gssapi-heimdal
  libsasl2-modules-ldap libsasl2-modules-otp libsasl2-modules-sql keychain
  libpam-ssh monkeysphere ssh-askpass ed diffutils-doc perl-doc
  libterm-readline-gnu-perl | libterm-readline-perl-perl make
  libtap-harness-archive-perl
The following NEW packages will be installed:
  git git-man less libbrotli1 libbsd0 libcbor0 libcurl3-gnutls libedit2
  liberror-perl libexpat1 libffi-dev libfido2-1 libgdbm-compat4 libgdbm6
  libldap-2.4-2 libldap-common libmd0 libnghttp2-14 libperl5.32 libpsl5
  librtmp1 libsasl2-2 libsasl2-modules libsasl2-modules-db libssh2-1 libx11-6
  libx11-data libxau6 libxcb1 libxdmcp6 libxext6 libxmuu1 netbase
  openssh-client patch perl perl-modules-5.32 publicsuffix xauth
0 upgraded, 39 newly installed, 0 to remove and 17 not upgraded.
Need to get 19.5 MB of archives.
After this operation, 99.7 MB of additional disk space will be used.
Get:1 http://deb.debian.org/debian bullseye/main amd64 perl-modules-5.32 all 5.32.1-4+deb11u2 [2823 kB]
Get:2 http://deb.debian.org/debian bullseye/main amd64 libgdbm6 amd64 1.19-2 [64.9 kB]
Get:3 http://deb.debian.org/debian bullseye/main amd64 libgdbm-compat4 amd64 1.19-2 [44.7 kB]
Get:4 http://deb.debian.org/debian bullseye/main amd64 libperl5.32 amd64 5.32.1-4+deb11u2 [4106 kB]
Get:5 http://deb.debian.org/debian bullseye/main amd64 perl amd64 5.32.1-4+deb11u2 [293 kB]
Get:6 http://deb.debian.org/debian bullseye/main amd64 less amd64 551-2 [133 kB]
Get:7 http://deb.debian.org/debian bullseye/main amd64 netbase all 6.3 [19.9 kB]
Get:8 http://deb.debian.org/debian bullseye/main amd64 libmd0 amd64 1.0.3-3 [28.0 kB]
Get:9 http://deb.debian.org/debian bullseye/main amd64 libbsd0 amd64 0.11.3-1+deb11u1 [108 kB]
Get:10 http://deb.debian.org/debian bullseye/main amd64 libedit2 amd64 3.1-20191231-2+b1 [96.7 kB]
Get:11 http://deb.debian.org/debian bullseye/main amd64 libcbor0 amd64 0.5.0+dfsg-2 [24.0 kB]
Get:12 http://deb.debian.org/debian bullseye/main amd64 libfido2-1 amd64 1.6.0-2 [53.3 kB]
Get:13 http://deb.debian.org/debian bullseye/main amd64 openssh-client amd64 1:8.4p1-5+deb11u2 [930 kB]
Get:14 http://deb.debian.org/debian bullseye/main amd64 libbrotli1 amd64 1.0.9-2+b2 [279 kB]
Get:15 http://deb.debian.org/debian bullseye/main amd64 libsasl2-modules-db amd64 2.1.27+dfsg-2.1+deb11u1 [69.1 kB]
Get:16 http://deb.debian.org/debian bullseye/main amd64 libsasl2-2 amd64 2.1.27+dfsg-2.1+deb11u1 [106 kB]
Get:17 http://deb.debian.org/debian bullseye/main amd64 libldap-2.4-2 amd64 2.4.57+dfsg-3+deb11u1 [232 kB]
Get:18 http://deb.debian.org/debian-security bullseye-security/main amd64 libnghttp2-14 amd64 1.43.0-1+deb11u1 [77.2 kB]
Get:19 http://deb.debian.org/debian bullseye/main amd64 libpsl5 amd64 0.21.0-1.2 [57.3 kB]
Get:20 http://deb.debian.org/debian bullseye/main amd64 librtmp1 amd64 2.4+20151223.gitfa8646d.1-2+b2 [60.8 kB]
Get:21 http://deb.debian.org/debian bullseye/main amd64 libssh2-1 amd64 1.9.0-2 [156 kB]
Get:22 http://deb.debian.org/debian-security bullseye-security/main amd64 libcurl3-gnutls amd64 7.74.0-1.3+deb11u10 [344 kB]
Get:23 http://deb.debian.org/debian bullseye/main amd64 libexpat1 amd64 2.2.10-2+deb11u5 [98.2 kB]
Get:24 http://deb.debian.org/debian bullseye/main amd64 liberror-perl all 0.17029-1 [31.0 kB]
Get:25 http://deb.debian.org/debian bullseye/main amd64 git-man all 1:2.30.2-1+deb11u2 [1828 kB]
Get:26 http://deb.debian.org/debian bullseye/main amd64 git amd64 1:2.30.2-1+deb11u2 [5518 kB]
Get:27 http://deb.debian.org/debian bullseye/main amd64 libffi-dev amd64 3.3-6 [56.5 kB]
Get:28 http://deb.debian.org/debian bullseye/main amd64 libldap-common all 2.4.57+dfsg-3+deb11u1 [95.8 kB]
Get:29 http://deb.debian.org/debian bullseye/main amd64 libsasl2-modules amd64 2.1.27+dfsg-2.1+deb11u1 [104 kB]
Get:30 http://deb.debian.org/debian bullseye/main amd64 libxau6 amd64 1:1.0.9-1 [19.7 kB]
Get:31 http://deb.debian.org/debian bullseye/main amd64 libxdmcp6 amd64 1:1.1.2-3 [26.3 kB]
Get:32 http://deb.debian.org/debian bullseye/main amd64 libxcb1 amd64 1.14-3 [140 kB]
Get:33 http://deb.debian.org/debian-security bullseye-security/main amd64 libx11-data all 2:1.7.2-1+deb11u2 [311 kB]
Get:34 http://deb.debian.org/debian-security bullseye-security/main amd64 libx11-6 amd64 2:1.7.2-1+deb11u2 [772 kB]
Get:35 http://deb.debian.org/debian bullseye/main amd64 libxext6 amd64 2:1.3.3-1.1 [52.7 kB]
Get:36 http://deb.debian.org/debian bullseye/main amd64 libxmuu1 amd64 2:1.1.2-2+b3 [23.9 kB]
Get:37 http://deb.debian.org/debian bullseye/main amd64 patch amd64 2.7.6-7 [128 kB]
Get:38 http://deb.debian.org/debian bullseye/main amd64 publicsuffix all 20220811.1734-0+deb11u1 [127 kB]
Get:39 http://deb.debian.org/debian bullseye/main amd64 xauth amd64 1:1.1-1 [40.5 kB]
debconf: delaying package configuration, since apt-utils is not installed
Fetched 19.5 MB in 0s (86.2 MB/s)
Selecting previously unselected package perl-modules-5.32.
(Reading database ... 6988 files and directories currently installed.)
Preparing to unpack .../00-perl-modules-5.32_5.32.1-4+deb11u2_all.deb ...
Unpacking perl-modules-5.32 (5.32.1-4+deb11u2) ...
Selecting previously unselected package libgdbm6:amd64.
Preparing to unpack .../01-libgdbm6_1.19-2_amd64.deb ...
Unpacking libgdbm6:amd64 (1.19-2) ...
Selecting previously unselected package libgdbm-compat4:amd64.
Preparing to unpack .../02-libgdbm-compat4_1.19-2_amd64.deb ...
Unpacking libgdbm-compat4:amd64 (1.19-2) ...
Selecting previously unselected package libperl5.32:amd64.
Preparing to unpack .../03-libperl5.32_5.32.1-4+deb11u2_amd64.deb ...
Unpacking libperl5.32:amd64 (5.32.1-4+deb11u2) ...
Selecting previously unselected package perl.
Preparing to unpack .../04-perl_5.32.1-4+deb11u2_amd64.deb ...
Unpacking perl (5.32.1-4+deb11u2) ...
Selecting previously unselected package less.
Preparing to unpack .../05-less_551-2_amd64.deb ...
Unpacking less (551-2) ...
Selecting previously unselected package netbase.
Preparing to unpack .../06-netbase_6.3_all.deb ...
Unpacking netbase (6.3) ...
Selecting previously unselected package libmd0:amd64.
Preparing to unpack .../07-libmd0_1.0.3-3_amd64.deb ...
Unpacking libmd0:amd64 (1.0.3-3) ...
Selecting previously unselected package libbsd0:amd64.
Preparing to unpack .../08-libbsd0_0.11.3-1+deb11u1_amd64.deb ...
Unpacking libbsd0:amd64 (0.11.3-1+deb11u1) ...
Selecting previously unselected package libedit2:amd64.
Preparing to unpack .../09-libedit2_3.1-20191231-2+b1_amd64.deb ...
Unpacking libedit2:amd64 (3.1-20191231-2+b1) ...
Selecting previously unselected package libcbor0:amd64.
Preparing to unpack .../10-libcbor0_0.5.0+dfsg-2_amd64.deb ...
Unpacking libcbor0:amd64 (0.5.0+dfsg-2) ...
Selecting previously unselected package libfido2-1:amd64.
Preparing to unpack .../11-libfido2-1_1.6.0-2_amd64.deb ...
Unpacking libfido2-1:amd64 (1.6.0-2) ...
Selecting previously unselected package openssh-client.
Preparing to unpack .../12-openssh-client_1%3a8.4p1-5+deb11u2_amd64.deb ...
Unpacking openssh-client (1:8.4p1-5+deb11u2) ...
Selecting previously unselected package libbrotli1:amd64.
Preparing to unpack .../13-libbrotli1_1.0.9-2+b2_amd64.deb ...
Unpacking libbrotli1:amd64 (1.0.9-2+b2) ...
Selecting previously unselected package libsasl2-modules-db:amd64.
Preparing to unpack .../14-libsasl2-modules-db_2.1.27+dfsg-2.1+deb11u1_amd64.deb ...
Unpacking libsasl2-modules-db:amd64 (2.1.27+dfsg-2.1+deb11u1) ...
Selecting previously unselected package libsasl2-2:amd64.
Preparing to unpack .../15-libsasl2-2_2.1.27+dfsg-2.1+deb11u1_amd64.deb ...
Unpacking libsasl2-2:amd64 (2.1.27+dfsg-2.1+deb11u1) ...
Selecting previously unselected package libldap-2.4-2:amd64.
Preparing to unpack .../16-libldap-2.4-2_2.4.57+dfsg-3+deb11u1_amd64.deb ...
Unpacking libldap-2.4-2:amd64 (2.4.57+dfsg-3+deb11u1) ...
Selecting previously unselected package libnghttp2-14:amd64.
Preparing to unpack .../17-libnghttp2-14_1.43.0-1+deb11u1_amd64.deb ...
Unpacking libnghttp2-14:amd64 (1.43.0-1+deb11u1) ...
Selecting previously unselected package libpsl5:amd64.
Preparing to unpack .../18-libpsl5_0.21.0-1.2_amd64.deb ...
Unpacking libpsl5:amd64 (0.21.0-1.2) ...
Selecting previously unselected package librtmp1:amd64.
Preparing to unpack .../19-librtmp1_2.4+20151223.gitfa8646d.1-2+b2_amd64.deb ...
Unpacking librtmp1:amd64 (2.4+20151223.gitfa8646d.1-2+b2) ...
Selecting previously unselected package libssh2-1:amd64.
Preparing to unpack .../20-libssh2-1_1.9.0-2_amd64.deb ...
Unpacking libssh2-1:amd64 (1.9.0-2) ...
Selecting previously unselected package libcurl3-gnutls:amd64.
Preparing to unpack .../21-libcurl3-gnutls_7.74.0-1.3+deb11u10_amd64.deb ...
Unpacking libcurl3-gnutls:amd64 (7.74.0-1.3+deb11u10) ...
Selecting previously unselected package libexpat1:amd64.
Preparing to unpack .../22-libexpat1_2.2.10-2+deb11u5_amd64.deb ...
Unpacking libexpat1:amd64 (2.2.10-2+deb11u5) ...
Selecting previously unselected package liberror-perl.
Preparing to unpack .../23-liberror-perl_0.17029-1_all.deb ...
Unpacking liberror-perl (0.17029-1) ...
Selecting previously unselected package git-man.
Preparing to unpack .../24-git-man_1%3a2.30.2-1+deb11u2_all.deb ...
Unpacking git-man (1:2.30.2-1+deb11u2) ...
Selecting previously unselected package git.
Preparing to unpack .../25-git_1%3a2.30.2-1+deb11u2_amd64.deb ...
Unpacking git (1:2.30.2-1+deb11u2) ...
Selecting previously unselected package libffi-dev:amd64.
Preparing to unpack .../26-libffi-dev_3.3-6_amd64.deb ...
Unpacking libffi-dev:amd64 (3.3-6) ...
Selecting previously unselected package libldap-common.
Preparing to unpack .../27-libldap-common_2.4.57+dfsg-3+deb11u1_all.deb ...
Unpacking libldap-common (2.4.57+dfsg-3+deb11u1) ...
Selecting previously unselected package libsasl2-modules:amd64.
Preparing to unpack .../28-libsasl2-modules_2.1.27+dfsg-2.1+deb11u1_amd64.deb ...
Unpacking libsasl2-modules:amd64 (2.1.27+dfsg-2.1+deb11u1) ...
Selecting previously unselected package libxau6:amd64.
Preparing to unpack .../29-libxau6_1%3a1.0.9-1_amd64.deb ...
Unpacking libxau6:amd64 (1:1.0.9-1) ...
Selecting previously unselected package libxdmcp6:amd64.
Preparing to unpack .../30-libxdmcp6_1%3a1.1.2-3_amd64.deb ...
Unpacking libxdmcp6:amd64 (1:1.1.2-3) ...
Selecting previously unselected package libxcb1:amd64.
Preparing to unpack .../31-libxcb1_1.14-3_amd64.deb ...
Unpacking libxcb1:amd64 (1.14-3) ...
Selecting previously unselected package libx11-data.
Preparing to unpack .../32-libx11-data_2%3a1.7.2-1+deb11u2_all.deb ...
Unpacking libx11-data (2:1.7.2-1+deb11u2) ...
Selecting previously unselected package libx11-6:amd64.
Preparing to unpack .../33-libx11-6_2%3a1.7.2-1+deb11u2_amd64.deb ...
Unpacking libx11-6:amd64 (2:1.7.2-1+deb11u2) ...
Selecting previously unselected package libxext6:amd64.
Preparing to unpack .../34-libxext6_2%3a1.3.3-1.1_amd64.deb ...
Unpacking libxext6:amd64 (2:1.3.3-1.1) ...
Selecting previously unselected package libxmuu1:amd64.
Preparing to unpack .../35-libxmuu1_2%3a1.1.2-2+b3_amd64.deb ...
Unpacking libxmuu1:amd64 (2:1.1.2-2+b3) ...
Selecting previously unselected package patch.
Preparing to unpack .../36-patch_2.7.6-7_amd64.deb ...
Unpacking patch (2.7.6-7) ...
Selecting previously unselected package publicsuffix.
Preparing to unpack .../37-publicsuffix_20220811.1734-0+deb11u1_all.deb ...
Unpacking publicsuffix (20220811.1734-0+deb11u1) ...
Selecting previously unselected package xauth.
Preparing to unpack .../38-xauth_1%3a1.1-1_amd64.deb ...
Unpacking xauth (1:1.1-1) ...
Setting up libexpat1:amd64 (2.2.10-2+deb11u5) ...
Setting up libxau6:amd64 (1:1.0.9-1) ...
Setting up libpsl5:amd64 (0.21.0-1.2) ...
Setting up perl-modules-5.32 (5.32.1-4+deb11u2) ...
Setting up libbrotli1:amd64 (1.0.9-2+b2) ...
Setting up libcbor0:amd64 (0.5.0+dfsg-2) ...
Setting up libsasl2-modules:amd64 (2.1.27+dfsg-2.1+deb11u1) ...
Setting up libnghttp2-14:amd64 (1.43.0-1+deb11u1) ...
Setting up less (551-2) ...
Setting up libffi-dev:amd64 (3.3-6) ...
Setting up libldap-common (2.4.57+dfsg-3+deb11u1) ...
Setting up libsasl2-modules-db:amd64 (2.1.27+dfsg-2.1+deb11u1) ...
Setting up libx11-data (2:1.7.2-1+deb11u2) ...
Setting up librtmp1:amd64 (2.4+20151223.gitfa8646d.1-2+b2) ...
Setting up patch (2.7.6-7) ...
Setting up libsasl2-2:amd64 (2.1.27+dfsg-2.1+deb11u1) ...
Setting up libmd0:amd64 (1.0.3-3) ...
Setting up git-man (1:2.30.2-1+deb11u2) ...
Setting up libssh2-1:amd64 (1.9.0-2) ...
Setting up netbase (6.3) ...
Setting up libfido2-1:amd64 (1.6.0-2) ...
Setting up libbsd0:amd64 (0.11.3-1+deb11u1) ...
Setting up publicsuffix (20220811.1734-0+deb11u1) ...
Setting up libgdbm6:amd64 (1.19-2) ...
Setting up libxdmcp6:amd64 (1:1.1.2-3) ...
Setting up libxcb1:amd64 (1.14-3) ...
Setting up libedit2:amd64 (3.1-20191231-2+b1) ...
Setting up libldap-2.4-2:amd64 (2.4.57+dfsg-3+deb11u1) ...
Setting up libcurl3-gnutls:amd64 (7.74.0-1.3+deb11u10) ...
Setting up libgdbm-compat4:amd64 (1.19-2) ...
Setting up libperl5.32:amd64 (5.32.1-4+deb11u2) ...
Setting up libx11-6:amd64 (2:1.7.2-1+deb11u2) ...
Setting up libxmuu1:amd64 (2:1.1.2-2+b3) ...
Setting up openssh-client (1:8.4p1-5+deb11u2) ...
Setting up libxext6:amd64 (2:1.3.3-1.1) ...
Setting up perl (5.32.1-4+deb11u2) ...
Setting up xauth (1:1.1-1) ...
Setting up liberror-perl (0.17029-1) ...
Setting up git (1:2.30.2-1+deb11u2) ...
Processing triggers for libc-bin (2.31-13+deb11u6) ...
Collecting apache-beam[gcp]
  Downloading apache_beam-2.48.0-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (13.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 13.5/13.5 MB 170.9 MB/s eta 0:00:00
Requirement already satisfied: typing-extensions>=3.7.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (4.5.0)
Requirement already satisfied: cloudpickle~=2.2.1 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.2.1)
Requirement already satisfied: hdfs<3.0.0,>=2.1.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: regex>=2020.6.8 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2022.10.31)
Requirement already satisfied: httplib2<0.23.0,>=0.8 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.21.0)
Requirement already satisfied: fastavro<2,>=0.23.6 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.7.3)
Requirement already satisfied: pytz>=2018.3 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2023.3)
Requirement already satisfied: proto-plus<2,>=1.7.1 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.22.2)
Requirement already satisfied: zstandard<1,>=0.18.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.20.0)
Requirement already satisfied: fasteners<1.0,>=0.3 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.18)
Requirement already satisfied: objsize<0.7.0,>=0.6.1 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.6.1)
Requirement already satisfied: crcmod<2.0,>=1.7 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.7)
Requirement already satisfied: numpy<1.25.0,>=1.14.3 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.21.6)
Requirement already satisfied: orjson<4.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.8.9)
Requirement already satisfied: pyarrow<12.0.0,>=3.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (11.0.0)
Requirement already satisfied: pydot<2,>=1.2.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.4.2)
Requirement already satisfied: requests<3.0.0,>=2.24.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.28.2)
Requirement already satisfied: pymongo<5.0.0,>=3.8.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (4.3.3)
Requirement already satisfied: protobuf<4.24.0,>=3.20.3 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (4.22.1)
Requirement already satisfied: grpcio!=1.48.0,<2,>=1.33.1 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.53.0)
Requirement already satisfied: python-dateutil<3,>=2.8.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.8.2)
Requirement already satisfied: dill<0.3.2,>=0.3.1.1 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.3.1.1)
Requirement already satisfied: google-apitools<0.5.32,>=0.5.31 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.5.31)
Requirement already satisfied: google-auth-httplib2<0.2.0,>=0.1.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.1.0)
Requirement already satisfied: google-cloud-bigquery<4,>=2.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.9.0)
Requirement already satisfied: google-cloud-bigquery-storage<3,>=2.6.3 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.19.1)
Requirement already satisfied: google-cloud-pubsub<3,>=2.1.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.15.2)
Requirement already satisfied: google-cloud-vision<4,>=2 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.4.1)
Requirement already satisfied: google-cloud-pubsublite<2,>=1.2.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.7.0)
Requirement already satisfied: google-cloud-recommendations-ai<0.11.0,>=0.1.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.10.3)
Requirement already satisfied: google-cloud-datastore<3,>=2.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.15.1)
Requirement already satisfied: cachetools<6,>=3.1.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (4.2.4)
Requirement already satisfied: google-cloud-spanner<4,>=3.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.30.0)
Requirement already satisfied: google-auth<3,>=1.18.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.17.1)
Requirement already satisfied: google-cloud-language<3,>=2.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.9.1)
Requirement already satisfied: google-cloud-dlp<4,>=3.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.12.1)
Requirement already satisfied: google-cloud-core<3,>=2.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.3.2)
Requirement already satisfied: google-cloud-bigtable<2.18.0,>=2.0.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.17.0)
Requirement already satisfied: google-cloud-videointelligence<3,>=2.0 in /usr/local/lib/python3.7/site-packages (from apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.11.1)
Requirement already satisfied: six>=1.12.0 in /usr/local/lib/python3.7/site-packages (from google-apitools<0.5.32,>=0.5.31->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.16.0)
Requirement already satisfied: oauth2client>=1.4.12 in /usr/local/lib/python3.7/site-packages (from google-apitools<0.5.32,>=0.5.31->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (4.1.3)
Requirement already satisfied: pyasn1-modules>=0.2.1 in /usr/local/lib/python3.7/site-packages (from google-auth<3,>=1.18.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.2.8)
Requirement already satisfied: rsa<5,>=3.1.4 in /usr/local/lib/python3.7/site-packages (from google-auth<3,>=1.18.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (4.9)
Requirement already satisfied: google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0dev,>=1.31.5 in /usr/local/lib/python3.7/site-packages (from google-cloud-bigquery<4,>=2.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.11.0)
Requirement already satisfied: packaging>=20.0.0 in /usr/local/lib/python3.7/site-packages (from google-cloud-bigquery<4,>=2.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (23.0)
Requirement already satisfied: google-resumable-media<3.0dev,>=0.6.0 in /usr/local/lib/python3.7/site-packages (from google-cloud-bigquery<4,>=2.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.4.1)
Requirement already satisfied: grpc-google-iam-v1<1.0.0dev,>=0.12.4 in /usr/local/lib/python3.7/site-packages (from google-cloud-bigtable<2.18.0,>=2.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.12.6)
Requirement already satisfied: grpcio-status>=1.33.2 in /usr/local/lib/python3.7/site-packages (from google-cloud-pubsub<3,>=2.1.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.53.0)
Requirement already satisfied: overrides<7.0.0,>=6.0.1 in /usr/local/lib/python3.7/site-packages (from google-cloud-pubsublite<2,>=1.2.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (6.5.0)
Requirement already satisfied: sqlparse>=0.3.0 in /usr/local/lib/python3.7/site-packages (from google-cloud-spanner<4,>=3.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.4.3)
Requirement already satisfied: docopt in /usr/local/lib/python3.7/site-packages (from hdfs<3.0.0,>=2.1.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.6.2)
Requirement already satisfied: pyparsing!=3.0.0,!=3.0.1,!=3.0.2,!=3.0.3,<4,>=2.4.2 in /usr/local/lib/python3.7/site-packages (from httplib2<0.23.0,>=0.8->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.0.9)
Requirement already satisfied: dnspython<3.0.0,>=1.16.0 in /usr/local/lib/python3.7/site-packages (from pymongo<5.0.0,>=3.8.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2.3.0)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/site-packages (from requests<3.0.0,>=2.24.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (2022.12.7)
Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.7/site-packages (from requests<3.0.0,>=2.24.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.4)
Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.7/site-packages (from requests<3.0.0,>=2.24.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (3.1.0)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.7/site-packages (from requests<3.0.0,>=2.24.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.26.15)
Requirement already satisfied: googleapis-common-protos<2.0dev,>=1.56.2 in /usr/local/lib/python3.7/site-packages (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0dev,>=1.31.5->google-cloud-bigquery<4,>=2.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.59.0)
Requirement already satisfied: google-crc32c<2.0dev,>=1.0 in /usr/local/lib/python3.7/site-packages (from google-resumable-media<3.0dev,>=0.6.0->google-cloud-bigquery<4,>=2.0.0->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (1.5.0)
Requirement already satisfied: pyasn1>=0.1.7 in /usr/local/lib/python3.7/site-packages (from oauth2client>=1.4.12->google-apitools<0.5.32,>=0.5.31->apache-beam[gcp]->-r /template/requirements.txt (line 1)) (0.4.8)
Installing collected packages: apache-beam
Successfully installed apache-beam-2.48.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

[notice] A new release of pip is available: 23.0.1 -> 23.3.1
[notice] To update, run: pip install --upgrade pip
Removing intermediate container 25694eb09539
 ---> 8d358260416a
Successfully built 8d358260416a
Successfully tagged australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:latest
PUSH
Pushing australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:latest
The push refers to repository [australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit]
24383711587b: Preparing
c51a98a27abc: Preparing
8fa78d98c59e: Preparing
7de9012aba24: Preparing
9173b60238cd: Preparing
fe8a9769ff1c: Preparing
6dd2e8cf7aeb: Preparing
91688c43606f: Preparing
03709403d38c: Preparing
3750dba27e3e: Preparing
fcf5fd93de52: Preparing
5f64b01c2f30: Preparing
a575c2d3bd67: Preparing
f31a073389cc: Preparing
ff1dbfd80a87: Preparing
1678f7d77690: Preparing
219c6c2423f1: Preparing
3af14c9a24c9: Preparing
fe8a9769ff1c: Waiting
6dd2e8cf7aeb: Waiting
91688c43606f: Waiting
03709403d38c: Waiting
5f64b01c2f30: Waiting
a575c2d3bd67: Waiting
3750dba27e3e: Waiting
f31a073389cc: Waiting
ff1dbfd80a87: Waiting
fcf5fd93de52: Waiting
219c6c2423f1: Waiting
3af14c9a24c9: Waiting
1678f7d77690: Waiting
9173b60238cd: Layer already exists
8fa78d98c59e: Layer already exists
7de9012aba24: Layer already exists
fe8a9769ff1c: Layer already exists
c51a98a27abc: Pushed
6dd2e8cf7aeb: Pushed
03709403d38c: Pushed
91688c43606f: Pushed
3750dba27e3e: Pushed
24383711587b: Pushed
ff1dbfd80a87: Pushed
f31a073389cc: Pushed
219c6c2423f1: Pushed
1678f7d77690: Pushed
a575c2d3bd67: Pushed
3af14c9a24c9: Pushed
fcf5fd93de52: Pushed
5f64b01c2f30: Pushed
latest: digest: sha256:e99c7de9a0403e8ba26cc67d83f1c0f59671446243eaea137cef4a58c038daf3 size: 4110
DONE
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
Successfully saved container spec in flex template file.
Template File GCS Location: gs://bkt-flex-test/flex/hellofruit.json
Container Spec:

{
    "defaultEnvironment": {
        "stagingLocation": "gs://bkt-flex-test/flex/staging",
        "tempLocation": "gs://bkt-flex-test/flex/tmp"
    },
    "image": "australia-southeast1-docker.pkg.dev/<project-id>/repo-docker/hellofruit:latest",
    "metadata": {
        "description": "Hello fruit Python flex template.",
        "name": "Hello fruit",
        "parameters": [
            {
                "helpText": "Name of the BigQuery output table name.",
                "isOptional": true,
                "label": "BigQuery output table name.",
                "name": "output_table",
                "regexes": [
                    "([^:]+:)?[^.]+[.].+"
                ]
            }
        ]
    },
    "sdkInfo": {
        "language": "PYTHON"
    }
}
```

