"""
Compliance audit trail logging service implementing cryptographic hash chaining.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit import AuditLog
import hashlib
import hmac
import json
import datetime
import uuid

class AuditService:
    async def log_action(
        self, 
        db: AsyncSession, 
        session_id: Optional_str = None,
        customer_id: Optional_str = None,
        agent_name: str = "Core",
        action_type: str = "System_Action",
        action_detail: dict = None,
        risk_tier: int = 1,
        autonomous: bool = False,
        outcome: str = "success"
    ) -> AuditLog:
        """
        Logs a transaction action to the audit log table, linking it via a SHA-256 hash chain.
        """
        detail_json = action_detail or {}
        
        # 1. Retrieve the previous hash block from the DB
        stmt = select(AuditLog.sha256_hash).order_by(AuditLog.created_at.desc()).limit(1)
        result = await db.execute(stmt)
        prev_hash = result.scalar_one_or_none() or "0000000000000000000000000000000000000000000000000000000000000000"
        
        # 2. Construct the data block payload
        timestamp_str = datetime.datetime.utcnow().isoformat()
        detail_str = json.dumps(detail_json, sort_keys=True)
        block_data = f"{prev_hash}|{timestamp_str}|{action_type}|{detail_str}"
        
        # 3. Compute SHA-256 Hash
        new_hash = hashlib.sha256(block_data.encode("utf-8")).hexdigest()
        
        # 4. Generate Mock signature (HSM Mock signature)
        # Using a dummy signing key to represent the HSM custody signature
        sig_key = b"sbi_hsm_signing_key_anchor"
        signature = hmac.new(sig_key, new_hash.encode("utf-8"), hashlib.sha256).hexdigest()
        
        # 5. Insert audit log record
        audit_id = str(uuid.uuid4())
        # Convert UUID-like constraints if database strings
        log_entry = AuditLog(
            id=audit_id,
            session_id=session_id,
            customer_id=customer_id,
            agent_name=agent_name,
            action_type=action_type,
            action_detail=detail_json,
            risk_tier=risk_tier,
            autonomous=autonomous,
            outcome=outcome,
            sha256_hash=new_hash,
            signature=signature
        )
        
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        
        return log_entry

# Helper typing details
Optional_str = str | None
