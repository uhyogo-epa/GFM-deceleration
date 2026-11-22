# Shared study library. Including this file defines functions; it starts no runs.
include("model.jl")
using .GFMModel, OrdinaryDiffEq, DelimitedFiles, LinearAlgebra, TOML, SHA
using Base.Threads
const ROOT=normpath(joinpath(@__DIR__,".."))
const SECTION_INPUT=joinpath(ROOT,"studies/paper/inputs/fault_basin.toml")
function readcases(file)
    lines=readlines(file);headers=split(lines[1],',')
    [Dict(String(k)=>String(v) for (k,v) in zip(headers,split(l,','))) for l in lines[2:end] if !isempty(strip(l))]
end
function writecsv(path,header,rows)
    open(path,"w") do io
        println(io,join(header,','));for row in rows;println(io,join(row,','));end
    end
end
compress(path)=run(`gzip -f $path`)
filehash(path)=bytes2hex(sha256(read(path)))
function code_identity()
    files=vcat(sort(filter(p->endswith(p,".jl"),readdir(joinpath(ROOT,"src");join=true))),[joinpath(ROOT,p) for p in ["studies/paper/scripts/run.jl","studies/paper/scripts/basins.jl","studies/paper/scripts/fault_basins.jl","Project.toml","Manifest.toml"]])
    Dict(relpath(p,ROOT)=>filehash(p) for p in files)
end
function input_identity(row;section=nothing)
    seeds=get(STUDY["seeds"],row["case"],STUDY["seeds"]["main"])
    files=vcat(["studies/paper/inputs/study.toml","studies/paper/inputs/cases.csv","studies/paper/inputs/original_cases.csv","studies/paper/inputs/"*row["config"],seeds["pre"],seeds["post"]],section===nothing ? String[] : [section])
    Dict(p=>filehash(joinpath(ROOT,p)) for p in files)
end
function assert_hashes(hashes,label)
    for (path,expected) in hashes
        actual=isfile(joinpath(ROOT,path)) ? filehash(joinpath(ROOT,path)) : "missing"
        actual==expected || error("Stale $label: $path differs from the recorded result. Recompute into a new output directory; do not reuse the old result.")
    end
end
function verify_reference(folder)
    catalog=TOML.parsefile(joinpath(ROOT,"studies/paper/provenance/reproduction.toml"))
    assert_hashes(catalog["code"],"model/code")
    key=relpath(folder,ROOT)
    if haskey(catalog["datasets"],key)
        record=catalog["datasets"][key]
        assert_hashes(record["inputs"],"input")
        assert_hashes(record["files"],"saved data")
    else
        path=joinpath(folder,"run_record.toml");isfile(path) || error("No result identity: $folder")
        record=TOML.parsefile(path);assert_hashes(record["code"],"model/code");assert_hashes(record["inputs"],"input")
    end
    record
end
function prepare_output(dir,row;kind,section=nothing,resume=false,options=Dict())
    any(startswith(abspath(dir)*"/",joinpath(ROOT,p)*"/") for p in ["studies/paper/results","studies/paper/figures","studies/paper/inputs","studies/paper/provenance","src"]) && error("Reference/source directories are read-only outputs; choose --output under outputs/ or a temporary directory.")
    record=Dict("schema"=>1,"kind"=>kind,"case"=>row,"inputs"=>input_identity(row;section),"code"=>code_identity(),"options"=>options,"config_text"=>read(joinpath(ROOT,"studies/paper/inputs",row["config"]),String),"study_text"=>read(joinpath(ROOT,"studies/paper/inputs/study.toml"),String))
    if section!==nothing
        target=joinpath(result_root(),row["case"],"post_root.csv")
        record["inputs"][relpath(target,ROOT)]=filehash(target)
        record["section_text"]=read(joinpath(ROOT,section),String)
    end
    path=joinpath(dir,"run_record.toml")
    if isdir(dir) && !isempty(readdir(dir))
        resume && isfile(path) || error("Output already exists: $dir. Choose a new --output directory.")
        previous=TOML.parsefile(path)
        all(get(previous,k,nothing)==v for (k,v) in record) || error("Stale output: input/code/options mismatch in $dir")
    else
        mkpath(dir);open(path,"w") do io;TOML.print(io,record);end
    end
end
function finish_output(dir)
    path=joinpath(dir,"run_record.toml");record=TOML.parsefile(path)
    record["files"]=Dict(relpath(joinpath(dir,p),ROOT)=>filehash(joinpath(dir,p)) for p in readdir(dir) if isfile(joinpath(dir,p)) && p!="run_record.toml")
    open(path,"w") do io;TOML.print(io,record);end
end
function result_root()
    i=findfirst(==("--results"),ARGS)
    i===nothing ? joinpath(ROOT,"studies/paper/results") : abspath(ARGS[i+1])
end
function validation_output()
    i=findfirst(==("--output"),ARGS);dir=i===nothing ? joinpath(ROOT,"outputs/checks") : abspath(ARGS[i+1]);mkpath(dir);dir
end
include("analysis.jl")
include("simulation.jl")
include("sections.jl")
