import sys
import os
# src 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Vector3D import Vector3D

if __name__ == '__main__':
    a = Vector3D(2.0, 3.0, 4.0)
    b = Vector3D(1.0, 3.0, 5.0)
    s = 10

    print(a + b)
    print(a - b)
    print(a * s)
    print(a / s)
