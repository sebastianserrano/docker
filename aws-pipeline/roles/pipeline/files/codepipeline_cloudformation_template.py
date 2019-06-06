""" Generate CodePipeline through Cloudformation template """

from awacs.aws import (
    Allow,
    Policy,
    Principal,
    Statement
)
from awacs.sts import AssumeRole
from troposphere import (
    Ref,
    GetAtt,
    Template
)
from troposphere.codepipeline import (
    Actions,
    ActionTypeId,
    ArtifactStore,
    InputArtifacts,
    OutputArtifacts,
    Pipeline,
    Stages
)
from troposphere.iam import Role
from troposphere.iam import Policy as IAMPolicy
from troposphere.s3 import (
    Bucket,
    VersioningConfiguration
)

template = Template()
template.add_description("Portfolio pipeline template")

template.add_resource(Bucket(
    "S3Bucket",
    VersioningConfiguration=VersioningConfiguration(
        Status="Enabled"
    )
))

template.add_resource(Role(
    "PortfolioPipelineRole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("Service", ["codepipeline.amazonaws.com"])
            )
        ]
    ),
    Policies=[
        IAMPolicy(
            PolicyName="PortfolioCodePipeline",
            PolicyDocument={
                "Statement": [
                    {"Effect": "Allow", "Action": "cloudformation:*", "Resource": "*"},
                    {"Effect": "Allow", "Action": "codedeploy:*", "Resource": "*"},
                    {"Effect": "Allow", "Action": "codepipeline:*", "Resource": "*"},
                    {"Effect": "Allow", "Action": "iam:*", "Resource": "*"},
                    {"Effect": "Allow", "Action": "s3:*", "Resource": "*"}
                ]
            }
        )
    ]
))

template.add_resource(Pipeline(
    "PortfolioPipeline",
    RoleArn=GetAtt("PortfolioPipelineRole", "Arn"),
    ArtifactStore=ArtifactStore(
        Type="S3",
        Location=Ref("S3Bucket")
    ),
    Stages=[
        Stages(
            Name="Source",
            Actions=[
                Actions(
                    Name="Source",
                    ActionTypeId=ActionTypeId(
                        Category="Source",
                        Owner="ThirdParty",
                        Version="1",
                        Provider="GitHub"
                    ),
                    Configuration={
                        "Owner": "ToBeConfiguredLater",
                        "Repo": "ToBeConfiguredLater",
                        "Branch": "ToBeConfiguredLater",
                        "OAuthToken": "ToBeConfiguredLater"
                    },
                    OutputArtifacts=[
                        OutputArtifacts(
                            Name="Portfolio"
                        )
                    ]
                )
            ]
        ),
        Stages(
            Name="Test",
            Actions=[
                Actions(
                    Name="Test",
                    Region="us-east-2",
                    ActionTypeId=ActionTypeId(
                        Category="Test",
                        Owner="Custom",
                        Version="1",
                        Provider="Jenkins-Portfolio"
                    ),
                    Configuration={
                        "ProjectName":"Portfolio"
                    },
                    InputArtifacts=[
                        InputArtifacts(
                            Name="Portfolio",
                        ),
                    ]
                )
            ]
        ),
        Stages(
            Name="Staging",
            Actions=[
                Actions(
                    Name="Deploy",
                    ActionTypeId=ActionTypeId(
                        Category="Deploy",
                        Owner="AWS",
                        Version="1",
                        Provider="CodeDeploy"
                    ),
                    Configuration={
                        "ApplicationName": "portfolio",
                        "DeploymentGroupName": "staging-portfolio"
                    },
                    InputArtifacts=[
                        InputArtifacts(
                            Name="Portfolio",
                        ),
                    ]
                )
            ]
        ),
        Stages(
            Name="Approval",
            Actions=[
                Actions(
                    Name="Approval",
                    ActionTypeId=ActionTypeId(
                        Category="Approval",
                        Owner="AWS",
                        Version="1",
                        Provider="Manual"
                    ),
                    Configuration={},
                    InputArtifacts=[],
                )
            ]
        ),
        Stages(
            Name="Production",
            Actions=[
                Actions(
                    Name="Deploy",
                    ActionTypeId=ActionTypeId(
                        Category="Deploy",
                        Owner="AWS",
                        Version="1",
                        Provider="CodeDeploy"
                    ),
                    Configuration={
                        "ApplicationName": "portfolio",
                        "DeploymentGroupName": "production-portfolio"
                    },
                    InputArtifacts=[
                        InputArtifacts(
                            Name="Portfolio",
                        ),
                    ]
                )
            ]
        ),
    ]
))

print(template.to_json())
