from fastapi import Depends, HTTPException, status


def check_permissions(required_permission: str):
    def permission_dependency(user: dict = Depends(get_current_user)):
        if required_permission not in user.get("permissions", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
            )

    return permission_dependency
