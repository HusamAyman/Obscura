import secrets

from domain.interfaces.recovery_key_generator import RecoveryKeyGenerator


class SecureRecoveryKeyGenerator(RecoveryKeyGenerator):
    def generate(self) -> str:
        alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
        key = ''.join(secrets.choice(alphabet) for _ in range(24))
        return '-'.join(key[i:i+6] for i in range(0, 24, 6))