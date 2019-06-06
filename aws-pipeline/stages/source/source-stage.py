from troposphere.codepipeline import (
    Stages
)

sourceStage = Stages(
            Name="Source",
            Actions=[
                Actions(
                    Name="Source",
                    ActionTypeId=ActionTypeId(
                        Category="Source",
                        Owner="ThirdParty",
                        Version="1",
                        Provider="Github"
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
