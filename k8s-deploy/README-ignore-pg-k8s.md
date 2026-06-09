Ignore the k8s config for configuring Postres in a 
Kubernetes cluster.

This approach was copied from this
article https://www.digitalocean.com/community/tutorials/how-to-deploy-postgres-to-kubernetes-cluster
but this approach does not work. This creates multiple Postgres
servers sharing data files, it DOES NOT create an HA cluster.