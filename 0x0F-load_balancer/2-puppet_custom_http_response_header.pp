# Install HAProxy package
package { 'haproxy':
  ensure => installed,
}

# custom configuration for HAProxy
file { '/etc/haproxy/haproxy_custom.cfg':
  ensure  => present,
  content => @("EOF"
frontend http_front
    http-response set-header X-Served-By $HOSTNAME
EOF
),
 require => Package['haproxy'],
  notify  => Service['haproxy'],
}

# Include custom configuration in the HAProxy main configuration file
exec { 'include_custom_config':
  command => 'echo "import /etc/haproxy/haproxy_custom.cfg" >> /etc/haproxy/haproxy.cfg',
  creates => '/etc/haproxy/haproxy_custom.cfg',
  require => File['/etc/haproxy/haproxy_custom.cfg'],
  notify  => Service['haproxy'],
}

# Enable HAProxy init script
file { '/etc/default/haproxy':
  ensure  => present,
  content => "ENABLED=1",
  require => Package['haproxy'],
  notify  => Service['haproxy'],
}

# Update /etc/hosts with correct hostnames and IP addresses
file { '/etc/hosts':
  content => @("EOF"
127.0.0.1 localhost
100.26.168.235 150802-web-01
18.207.234.92 150802-web-02
# ... (other existing entries)
EOF
),
  require => Package['haproxy'],
}

# Validate HAProxy configuration before restart
exec { 'validate_haproxy_config':
  command => 'haproxy -c -f /etc/haproxy/haproxy.cfg',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  refreshonly => true,
  subscribe => File['/etc/haproxy/haproxy.cfg'],
  notify  => Service['haproxy'],
}

# Restart HAProxy service
service { 'haproxy':
  ensure    => running,
  enable    => true,
  subscribe => [File['/etc/haproxy/haproxy_custom.cfg'], File['/etc/hosts'], Exec['include_custom_config'], Exec['validate_haproxy_config']],
}

