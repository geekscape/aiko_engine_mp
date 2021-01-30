
if ([string]::IsNullOrEmpty($env:AMPY_PORT)) {
    $env:AMPY_PORT = 'COM9'
}

$MPF_SCRIPT = $args[0]



py $env:VIRTUAL_ENV\Scripts\mpfshell-script.py --reset -o $env:AMPY_PORT -s $MPF_SCRIPT
