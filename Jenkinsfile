pipeline {
    agent none 
    stages {
	stage('Build microservice') {
	    agent {
		docker {
		    image 'python:3.9-slim-bullseye'
		    args '-u 0'
	        }
	    }
	    steps {
		sh 'pip install pipenv-setup vistir==0.6.1'
		sh 'pipenv-setup sync'
		sh 'python setup.py bdist_wheel'
		stash includes: 'dist/**', name: 'app'
	    }
	}
	stage('Create image') {
	    agent any
	    environment {
                IMG_NAME = """${sh(
                    returnStdout: true,
                    script: 'echo "$REGISTRY_HOST/uf_chile/ms_uf_chile:dev$(date +\"_%y%m%d_%H%M%S\")"'
                )}"""
	    }
	    steps {
	        unstash 'app'
                sh 'cp instance/etc/config.example.yml instance/etc/config.yml'
		sh 'docker build -t micro_uf_chile:from_jenkins --build-arg VERSION=0.0.1 --build-arg EXPOSE_PORT=80 .'
                sh 'docker tag micro_uf_chile:from_jenkins ${IMG_NAME}'
                sh 'docker login ${REGISTRY_HOST} -u ${REGISTRY_USER} -p ${REGISTRY_PASS}'
                sh 'docker push ${IMG_NAME}'
                sh 'docker image rm -f ${IMG_NAME}'
                sh 'docker image rm -f micro_uf_chile:from_jenkins'
	    }
	}
    }
}
