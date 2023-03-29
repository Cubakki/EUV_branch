#bash生成器

def bash_g(path,platform,script_name):
    if platform=="PBS":
        order="qsub"
    else:
        order="sbatch"
    bash_text=  f"cd {path}\n" \
                f"{order} {script_name}\n"
    with open(path+"/natzme.sh","w") as f:
        f.write(bash_text)
        f.close()
    return path+"/natzme.sh"
