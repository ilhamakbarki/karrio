pipeline {
    agent {
        kubernetes {
          label 'kube-1'
        }
    }
    environment {
        DOCKER_IMAGE_BE = "otokarrio.api"
        DOCKER_IMAGE_FE = "otokarrio.dashboard"
        REGISTRY_HOST = credentials("DOCKER_REGISTRY_HOST")
        APPROVAL = credentials("APPROVAL_RELEASE")
        NOTIF_API_KEY = credentials('NOTIF_API_KEY')
    }
    stages {
        stage('Build & Push Image Staging & Deploy to Staging') {
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
                    docker.withRegistry("https://${REGISTRY_HOST}", "DOCKER_REGISTRY_USER") {
                        sh "docker push ${imageLatest}"
                        sh "docker tag ${imageLatest} ${imageBuildNumber}"
                        sh "docker push ${imageBuildNumber}"
                    }

                    echo "Start Deploy on Staging"
                    if (currentBranch.contains('staging_beta_fe')) {
                        sh "kubectl set image deployment karrio-fe-app karrio-fe-app=${imageBuildNumber} -n=karrio-fe-staging"
                    } else {
                        sh "kubectl set image deployment karrio-be-app karrio-be-app=${imageBuildNumber} -n=karrio-be-staging"
                        sh "kubectl set image deployment karrio-be-worker karrio-be-worker=${imageBuildNumber} -n=karrio-be-staging"
                    }
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
                    docker.withRegistry('https://${REGISTRY_HOST}', 'DOCKER_REGISTRY_USER') {
                        sh "docker push ${imageLatest}"
                        sh "docker tag ${imageLatest} ${imageBuildNumber}"
                        sh "docker push ${imageBuildNumber}"
                    }

                    echo "Start Deploy on Production"
                    if (currentBranch.contains('release-fe')) {
                        sh "kubectl set image deployment karrio-fe-app karrio-fe-app=${imageBuildNumber} -n=karrio-fe-production"
                    } else {
                        sh "kubectl set image deployment karrio-be-app karrio-be-app=${imageBuildNumber} -n=karrio-be-production"
                        sh "kubectl set image deployment karrio-be-worker karrio-be-worker=${imageBuildNumber} -n=karrio-be-production"
                    }
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
