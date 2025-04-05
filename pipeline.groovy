pipeline{
    agent {label 'node1'}
    
    environment {
        docker_img_name = 'adhmabdein/myflaskimg2'
    }
    
    stages{
        stage('pull code from github'){
            steps{
                script{
                    git "https://github.com/AdhmAbdein/flask-project-adv.git"
                    
                }
            }
        }
        stage('log in to docker hub'){
            steps{
                script{
                    withCredentials ([usernamePassword(credentialsId:'docker_hub', usernameVariable:'d_hub_usr', passwordVariable:'d_hub_pass')]){
                        sh 'docker login -u ${d_hub_usr} -p ${d_hub_pass}'
                    }
                }
            }
        }
        stage('CI - Build docker image'){
            steps{
                script{
                    sh 'docker build -t ${docker_img_name} -f project-code/Dockerfile .'
                }
            }
        }
        stage('push image to docker hub'){
            steps{
                script{
                    sh 'docker push ${docker_img_name}'
                }
            }
        }
        stage('CD - Deploy in k8s'){
            steps{
                script{
                    dir('project-code'){
                       sh 'kubectl apply -f k8s-postgres-pvpv.yml'
                       sh 'kubectl apply -f k8s-postgres-pvc.yml'
                       sh 'kubectl apply -f k8s-postgres-dep.yml'
                       sh 'kubectl apply -f k8s-postgres-svc.yml'
                       
                       sh 'kubectl apply -f k8s-flask-deploy.yml'
                       sh 'kubectl apply -f k8s-flask-svc.yml'
                    }
                }
            }
        }
       
    }
}