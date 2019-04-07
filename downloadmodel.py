from azureml.core import Workspace
from azureml.core.model import Model
import os 

from azureml.core.runconfig import RunConfiguration
from azureml.core.authentication import AzureCliAuthentication
cli_auth = AzureCliAuthentication()

# Get workspace
ws = Workspace.from_config(auth=cli_auth)

model = Model(ws, 'MyModel')

print(model.name)
print(os.getcwd())

result = model.download(target_dir=os.getcwd(), exist_ok=True)

print(result)
