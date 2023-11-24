def update_post_fields(post, new_info):
    for field, value in new_info.model_dump().items():
        setattr(post, field, value)
