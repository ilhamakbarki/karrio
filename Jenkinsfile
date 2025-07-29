pipeline {
    agent { label (env.BRANCH_NAME == 'staging_beta_be' || env.BRANCH_NAME == 'staging_beta_fe' ? 'agent-staging' : 'agent-production') }
    environment {
        DOCKER_IMAGE_BE = "otokarrio.api"
        DOCKER_IMAGE_FE = "otokarrio.dashboard"
        COMPOSE_FILE_BE = "/home/ubuntu/apps/oto/karrio-backend/docker-compose.yaml"
        COMPOSE_FILE_FE = "/home/ubuntu/apps/oto/karrio-frontend/docker-compose.yaml"
        REGISTRY_HOST = credentials("DOCKER_REGISTRY_HOST")
        REGISTRY_USER = "DOCKER_REGISTRY_USER"
        STAGING_HOST = credentials('HOST_STAGING')
        STAGING_USER = "USER_SERVER_STAGING"
        APPROVAL = credentials("APPROVAL_RELEASE")
        AWS_SCRIPT = credentials("AWS_AUTO_START_SCRIPT")
        CONFIG_BE_PROD_AWS = credentials("KARRIO_API_PROD_AWS_CONFIG")
        CONFIG_FE_PROD_AWS = credentials("KARRIO_FE_PROD_AWS_CONFIG")
        NOTIF_API_KEY = credentials('NOTIF_API_KEY')
    }
    stages {
        stage('Build & Push Image Staging & Remove Image') {
            when { branch 'staging_beta_*' }
            steps {
                script {
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: scm.branches,
                        doNotStripRemotePrefix: true,
                        userRemoteConfigs: scm.userRemoteConfigs
                    ]
                    echo "Main repository checked out. Now cloning specific submodule 'community'..."
                    sh 'git submodule update --init -- "community"'
                    def currentBranch = env.BRANCH_NAME
                    def DOCKER_TARGET_IMAGE = currentBranch.contains('staging_beta_fe') ? DOCKER_IMAGE_FE : DOCKER_IMAGE_BE
                    def imageLatest = "${REGISTRY_HOST}/${DOCKER_TARGET_IMAGE}:staging_beta-latest"
                    def imageBuildNumber = "${REGISTRY_HOST}/${DOCKER_TARGET_IMAGE}:staging_beta-${BUILD_NUMBER}"
                    if (currentBranch.contains('staging_beta_fe')) {
                        echo "Start Build Image ${DOCKER_TARGET_IMAGE} Staging"
                        sh "docker build -t ${imageLatest} -f docker/dashboard/Dockerfile.oto ."
                    } else if (currentBranch.contains('staging_beta_be')) {
                        echo "Start Build Image ${DOCKER_TARGET_IMAGE} Staging"
                        sh "docker build -t ${imageLatest} -f docker/api/Dockerfile.oto ."
                    } else {
                        error "Unsupported branch name for staging build: ${currentBranch}. Expected 'staging_beta_fe' or 'staging_beta_be'."
                    }

                    echo 'Start Pushing Image'
                    docker.withRegistry('https://${REGISTRY_HOST}', REGISTRY_USER) {
                        sh "docker push ${imageLatest}"
                        sh "docker tag ${imageLatest} ${imageBuildNumber}"
                        sh "docker push ${imageBuildNumber}"
                    }

                    echo "Removing image after push"
                    sh "docker rmi -f ${imageLatest}"
                    sh "docker rmi -f ${imageBuildNumber}"
                }
            }
        }
        stage('Publish Approval') {
            when { tag "release-*" }
            steps {
                script{
                    sendNotification("Waiting Approval to Deploy on Production")
                    def tagName = env.TAG_NAME
                    def approvers = APPROVAL.split(',')
                    def userName = input message: "Do you want to deploy ${tagName}?", submitter: APPROVAL, submitterParameter: "userName"

                    if (!approvers.contains(userName)) {
                        error('This user is not approved to deploy to PROD.')
                    } else {
                        echo "Accepted by ${userName}"
                    }
                }
            }
        }
        stage('Build & Push Image Production & Remove Image') {
            when { tag "release-*" }
            steps {
                script {
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: scm.branches,
                        doNotStripRemotePrefix: true,
                        userRemoteConfigs: scm.userRemoteConfigs
                    ]
                    echo "Main repository checked out. Now cloning specific submodule 'community'..."
                    sh 'git submodule update --init -- "community"'
                    def currentTag = env.TAG_NAME
                    def DOCKER_TARGET_IMAGE = currentTag.contains('release-fe') ? DOCKER_IMAGE_FE : DOCKER_IMAGE_BE
                    def imageLatest = "${REGISTRY_HOST}/${DOCKER_TARGET_IMAGE}:release-latest"
                    def imageBuildNumber = "${REGISTRY_HOST}/${DOCKER_TARGET_IMAGE}:${TAG_NAME}-${BUILD_NUMBER}"
                    if (currentTag.contains('release-fe')) {
                        echo "Start Build Image ${DOCKER_TARGET_IMAGE} Production"
                        sh "docker build -t ${imageLatest} -f docker/dashboard/Dockerfile.oto ."
                    } else if (currentTag.contains('release-be')) {
                        echo "Start Build Image ${DOCKER_TARGET_IMAGE} Production"
                        sh "docker build -t ${imageLatest} -f docker/api/Dockerfile.oto ."
                    }else {
                        error "Unsupported release build: ${currentTag}. Expected 'release-be-*' or 'release-fe-*'."
                    }

                    echo 'Start Pushing Image'
                    docker.withRegistry('https://${REGISTRY_HOST}', REGISTRY_USER) {
                        sh "docker push ${imageLatest}"
                        sh "docker tag ${imageLatest} ${imageBuildNumber}"
                        sh "docker push ${imageBuildNumber}"
                    }

                    echo "Removing image after push"
                    sh "docker rmi -f ${imageLatest}"
                    sh "docker rmi -f ${imageBuildNumber}"
                }
            }
        }
        stage('Clean Up Docker Images & Cache') {
            steps {
                script {
                    echo "Cleaning up Docker images and build cache"
                    sh "docker image prune -f"
                    sh "docker builder prune -f"
                    echo "Clean up completed!"
                }
            }
        }
        stage('Deploy BE on Staging') {
            when { branch 'staging_beta_*' }
            steps {
                echo 'Start Deploy on Staging'
                script {
                    sshagent(credentials: [STAGING_USER]) {
                        def DOCKER_IMAGE = env.BRANCH_NAME.contains('staging_beta_fe') ? DOCKER_IMAGE_FE : DOCKER_IMAGE_BE
                        def COMPOSE_FILE = env.BRANCH_NAME.contains('staging_beta_fe') ? COMPOSE_FILE_FE : COMPOSE_FILE_BE
                        sh """
                            ssh -o StrictHostKeyChecking=no ubuntu@${STAGING_HOST} '
                            docker compose -f ${COMPOSE_FILE} pull ${DOCKER_IMAGE} &&
                            docker compose -f ${COMPOSE_FILE} up -d &&
                            docker image prune -f'
                        """
                    }
                }
            }
        }
        stage('Deploy on Production') {
            when { tag "release-*" }
            steps {
                echo 'Starting Deploy on Production'
                script {
                    def CONFIG_PROD_AWS = env.TAG_NAME.contains('release-fe') ? CONFIG_FE_PROD_AWS : CONFIG_BE_PROD_AWS
                    sh '${AWS_SCRIPT} ${CONFIG_PROD_AWS}'
                }
            }
        }
    }

    post {
        success {
            script {
                sendNotification("Success to deploy.")
            }
        }
        failure {
            script {
                sendNotification("Failed to deploy.")
            }
        }
    }
}

def sendNotification(message) {
    echo 'Sending Notification...'
    def tag = env.TAG_NAME ?: ''
    def branch = env.BRANCH_NAME ?: ''
    def DOCKER_IMAGE = branch.contains('staging_beta_fe') || tag.contains('release-fe') ? DOCKER_IMAGE_FE : DOCKER_IMAGE_BE
    def NAME = env.TAG_NAME ?: env.BRANCH_NAME
    def cleanJobPath = env.JOB_NAME.replaceFirst('^/job', '').replaceAll('/$', '')
    def formattedJobPath = cleanJobPath.split('/').collect { "job/${it}" }.join('/')
    def link = "${env.JENKINS_URL}${formattedJobPath}/${env.BUILD_NUMBER}/console"
    sh """
        curl --location 'https://webhooks.socialbot.dev/webhook/jenkins-deploy' \\
            --header 'Content-Type: application/json' \\
            --header 'x-api-key: ${NOTIF_API_KEY}' \\
            --data '{
                "message": "${message} Link : ${link}",
                "service": "${DOCKER_IMAGE}",
                "branch": "${branch}",
                "tag": "${tag}"
            }'
    """
}

def generateDockerBuildArgs(envContent) {
    def buildArgs = []
    def lines = envContent.readLines()
    lines.each { line ->
        def trimmedLine = line.trim()

        if (trimmedLine && !trimmedLine.startsWith('#')) {
            def parts = trimmedLine.split('=', 2)
            if (parts.size() == 2) {
                def key = parts[0].trim()
                def value = parts[1].trim()
                if (value.startsWith('"') && value.endsWith('"')) {
                    value = value.substring(1, value.length() - 1)
                }
                buildArgs << "--build-arg ${key}=\"${value}\""
            } else {
                println "Warning: Skip invalid line format in .env: ${line}"
            }
        }
    }
    return buildArgs.join(' ')
}
