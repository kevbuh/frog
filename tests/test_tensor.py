import numpy as np
import torch
from frog.tensor import Tensor

x_init = np.random.randn(1,3).astype(np.float32)
W_init = np.random.randn(3,3).astype(np.float32)
m_init = np.random.randn(1,3).astype(np.float32)

def test_frog():
  x = Tensor(x_init)
  W = Tensor(W_init)
  m = Tensor(m_init)
  out = x.dot(W).relu()
  out = out.logsoftmax()
  out = out.mul(m).add(m).sum()
  out.backward()
  return out.data, x.grad, W.grad

def test_pytorch():
  x = torch.tensor(x_init, requires_grad=True)
  W = torch.tensor(W_init, requires_grad=True)
  m = torch.tensor(m_init)
  out = x.matmul(W).relu()
  out = torch.nn.functional.log_softmax(out, dim=1)
  out = out.mul(m).add(m).sum()
  out.backward()
  return out.detach().numpy(), x.grad, W.grad

for x,y in zip(test_frog(), test_pytorch()):
  # print("frog: ",x)
  # print("torch: ",y)
  np.testing.assert_allclose(x, y, atol=1e-5)

print("All tests passed!")