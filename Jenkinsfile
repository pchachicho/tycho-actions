library 'pipeline-utils@master'

CCV = ""

pipeline {
  agent {
    kubernetes {
        label 'kaniko-build-agent'
        yaml """
kind: Pod
metadata:
  name: kaniko
spec:
  containers:
  - name: jnlp
    workingDir: /home/jenkins/agent
  - name: go
    workingDir: /home/jenkins/agent
    image: golang:1.19.1
    imagePullPolicy: Always
    resources:
      requests:
        cpu: "512m"
        memory: "512Mi"
        ephemeral-storage: "1Gi"
      limits:
        cpu: "512m"
        memory: "1024Mi"
        ephemeral-storage: "1Gi"
    command:
    - /bin/bash
    tty: true
"""
        }
    }
    environment {
        PATH = "/busybox:/kaniko:/ko-app/:$PATH"
        DOCKERHUB_CREDS = credentials("${env.CONTAINERS_REGISTRY_CREDS_ID_STR}")
        REGISTRY = "${env.REGISTRY}"
        REG_OWNER="helxplatform"
        REPO_NAME="tycho"
        COMMIT_HASH="${sh(script:"git rev-parse --short HEAD", returnStdout: true).trim()}"
        IMAGE_NAME="${REGISTRY}/${REG_OWNER}/${REPO_NAME}"
    }
    stages {
        stage('Build') {
            steps {
                script {
                    container(name: 'go', shell: '/bin/bash') {
                        if (BRANCH_NAME.equals("master")) { 
                            CCV = go.ccv()
                        }
                    }
                }
            }
        }
    }
}
